from odoo import models, fields

class TimeSheet(models.Model):
    _name = 'time.sheet'
    _description = 'Time Sheet'

    date = fields.Date(default=fields.Date.today , required=True)
    hours = fields.Float(required=True)
    description = fields.Text(required=True)
    task_id = fields.Many2one('todo.task', required=True)