from odoo import fields, models
from odoo.exceptions import ValidationError


class TaskAssignmentWizard(models.TransientModel):
    _name = 'task.assignment.wizard'
    _description = 'Task Assignment Wizard'

    assigned_to = fields.Many2one('res.users',required=True)

    def action_assign_tasks(self):
        """
        Assign selected tasks to the chosen user.
        """
        self.ensure_one()

        active_ids = self.env.context.get('active_ids')

        if not active_ids:
            raise ValidationError(
                'Please select at least one task.'
            )

        tasks = self.env['todo.task'].browse(active_ids)

        tasks.write({
            'assigned_to': self.assigned_to.id
        })

        return {
            'type': 'ir.actions.act_window_close',
        }