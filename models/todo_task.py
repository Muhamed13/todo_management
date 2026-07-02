from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo App'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=True)
    name = fields.Char('Task Name', required=True, tracking=True)
    assigned_to = fields.Many2one('res.users', tracking=True)
    description = fields.Text()
    due_date = fields.Date(tracking=True)
    estimated_time = fields.Float('Estimated Time', required=True, tracking=True)
    timesheet_ids = fields.One2many(string='Timesheets', comodel_name="time.sheet", inverse_name="task_id")
    is_late = fields.Boolean()
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], default='new', tracking=True)
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours', store=True, readonly=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'Task name must be unique.')
    ]

    @api.depends('timesheet_ids.hours')
    def _compute_total_hours(self):
        """
           Calculate total logged hours from related timesheets.
        """
        for rec in self:
           rec.total_hours = sum(rec.timesheet_ids.mapped('hours'))

    @api.constrains('estimated_time', 'total_hours')
    def _check_estimated_time(self):
        """
            Prevent logged hours from exceeding estimated hours.
        """
        for rec in self:
            if rec.total_hours > rec.estimated_time:
                raise ValidationError('Total time cannot exceed estimated time.')


    # ------------------------------------------------------------------
    # State Actions
    # ------------------------------------------------------------------

    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'completed'

    def action_reset(self):
        for rec in self:
            rec.state = 'new'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'


    def _check_late_tasks(self):
        """
            Scheduled action that marks overdue tasks as late.
        """
        tasks = self.search([('state', '!=', 'closed')])
        for rec in tasks:
            if rec.due_date and rec.due_date < fields.Date.today():
                rec.is_late = True
            else:
                rec.is_late = False

    @api.model
    def create(self, vals):
        """
           Generate task reference using Odoo sequence.
        """
        if vals.get('ref', 'New') == 'New':
            vals['ref'] = self.env['ir.sequence'].next_by_code('todo_task_seq')

        return super().create(vals)

    def action_open_assignment_wizard(self):
        """
            Open task assignment wizard for selected tasks.
        """
        action = self.env.ref(
            'todo_management.task_assignment_wizard_action').read()[0]

        action['context'] = {'active_ids': self.ids,}
        return action

    def write(self, vals):
        """
            Prevent modifications on completed or closed tasks.
        """
        for rec in self:
            if rec.state in ['completed', 'closed']:
                raise ValidationError('You cannot modify a completed or closed task.')
        return super().write(vals)

