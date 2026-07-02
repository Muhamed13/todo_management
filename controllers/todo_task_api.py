from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import json

headers = [
    ('Content-Type', 'application/json')
]


class TodoTaskApi(http.Controller):

    @http.route('/api/v1/tasks', type='http', auth='none', methods=['POST'], csrf=False)
    def create_task(self, **kwargs):
        """
        Create a new task.
        """
        try:
            data = json.loads(request.httprequest.data or '{}')

            name = (data.get('name') or '').strip()
            description = data.get('description')
            assigned_to = data.get('assigned_to')
            due_date = data.get('due_date')
            estimated_time = data.get('estimated_time')

            # Required Fields Validation
            if not name:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Task name is required'
                    }), headers=headers, status=400)

            if estimated_time is None:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Estimated time is required'
                    }), headers=headers, status=400)

            # Business Validation
            if float(estimated_time) <= 0:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Estimated time must be greater than zero'
                    }), headers=headers, status=400)

            task = request.env['todo.task'].sudo().create({
                'name': name,
                'description': description,
                'assigned_to': assigned_to,
                'due_date': due_date,
                'estimated_time': estimated_time,
            })

            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': 'Task created successfully',
                    'data': {
                        'id': task.id,
                        'ref': task.ref,
                        'name': task.name,
                        'state': task.state,
                    }
                }),
                headers=headers, status=201)

        except ValidationError as error:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(error)
                }), headers=headers, status=400)

        except Exception as error:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(error)
                }), headers=headers, status=500)

    @http.route('/api/v1/tasks', type='http', auth='none', methods=['GET'], csrf=False)
    def get_tasks(self, **kwargs):
        """
        Retrieve all tasks.
        """
        try:
            tasks = request.env['todo.task'].sudo().search([])
            result = []

            for task in tasks:
                result.append({
                    'id': task.id,
                    'ref': task.ref,
                    'name': task.name,
                    'description': task.description,
                    'assigned_to': task.assigned_to.name if task.assigned_to else False,
                    'due_date': str(task.due_date) if task.due_date else False,
                    'estimated_time': task.estimated_time,
                    'state': task.state,
                })

            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': 'Tasks retrieved successfully',
                    'data': result
                }), headers=headers, status=200)

        except Exception as error:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(error)
                }), headers=headers, status=500)

    @http.route('/api/v1/tasks/<int:task_id>', type='http', auth='none', methods=['GET'], csrf=False)
    def get_task(self, task_id, **kwargs):
        """
        Retrieve a task by ID.
        """
        try:
            task = request.env['todo.task'].sudo().browse(task_id)

            if not task.exists():
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Task not found'
                    }), headers=headers, status=404)

            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': 'Task retrieved successfully',
                    'data': {
                        'id': task.id,
                        'ref': task.ref,
                        'name': task.name,
                        'description': task.description,
                        'assigned_to': task.assigned_to.name if task.assigned_to else False,
                        'due_date': str(task.due_date) if task.due_date else False,
                        'estimated_time': task.estimated_time,
                        'state': task.state,
                    }
                }), headers=headers, status=200)

        except Exception as error:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(error)
                }), headers=headers, status=500)

    @http.route('/api/v1/tasks/<int:task_id>', type='http', auth='none', methods=['PUT'], csrf=False)
    def update_task(self, task_id, **kwargs):
        """
        Update an existing task.
        """
        try:
            task = request.env['todo.task'].sudo().browse(task_id)

            if not task.exists():
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Task not found'
                    }), headers=headers, status=404)

            data = json.loads(request.httprequest.data)

            if 'name' in data and not data.get('name'):
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Task name cannot be empty'
                    }), headers=headers, status=400)

            if 'estimated_time' in data and data.get('estimated_time') <= 0:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Estimated time must be greater than zero'
                    }), headers=headers, status=400)

            task.write(data)

            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': 'Task updated successfully'
                }), headers=headers, status=200)

        except Exception as error:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(error)
                }), headers=headers, status=500)

    @http.route('/api/v1/tasks/<int:task_id>', type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_task(self, task_id, **kwargs):
        """
        Delete a task if it has no related timesheets.
        """
        try:
            task = request.env['todo.task'].sudo().browse(task_id)

            if not task.exists():
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Task not found'
                    }), headers=headers, status=404)

            if task.timesheet_ids:
                return request.make_response(
                    json.dumps({
                        'success': False,
                        'message': 'Cannot delete task because it has timesheet records'
                    }), headers=headers, status=400)

            task.unlink()

            return request.make_response(
                json.dumps({
                    'success': True,
                    'message': 'Task deleted successfully'
                }), headers=headers, status=200)

        except Exception as error:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(error)
                }), headers=headers, status=500)