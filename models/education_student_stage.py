from odoo import fields, models, api

class EducationStudentsStage(models.Model):
    _name = 'education.student.stage'
    _description = 'Education Student Stage'
    _order = 'sequence,name asc'
    
    name = fields.Char(string="Name")
    sequence = fields.Integer(string='Sequence')
    fold = fields.Boolean(string='Fold')
    
    student_state = fields.Char(string="Student state")