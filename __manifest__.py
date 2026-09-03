{
    'name': 'To-Do Management',
    'author': 'Muhamed Helmy',
    'version': '17.0.0.1.0',
    'category': 'Productivity',
    'license': 'LGPL-3',

    'summary': 'Task management with timesheets, reports, wizard and REST API',

    'description': """
Todo Management System

Features:
- Task Management
- Timesheet Tracking
- Task Assignment Wizard
- PDF Reports
- REST API
- User Security & Access Rules
""",

    'depends': [
        'base',
        'mail',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',

        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'views/time_sheet_view.xml',

        'wizard/assignment_wizard_view.xml',

        'reports/todo_task_report.xml',
    ],

    'application': True,
}