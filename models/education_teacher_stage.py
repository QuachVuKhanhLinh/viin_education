from odoo import models, fields, api

class EducationTeacherStage(models.Model):
    _name = 'education.teacher.stage'
    
    name = fields.Char(string='Name')
    sequence = fields.Integer(string='sequence')
    fold = fields.Boolean(string='Fold')
    
    teacher_state = fields.Char(string='State')