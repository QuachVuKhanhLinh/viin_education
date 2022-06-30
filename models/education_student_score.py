from odoo import models, fields, api

class EducationStudentScore(models.Model):
    _name = 'education.student.score'
    _description = 'Education Student Score'
    
    score = fields.Float(string='Score', digits=(12,2))
    student_code = fields.Char(string='Student code', related='student_id.student_code')
    student_name = fields.Char(string='Student name', related='student_id.name')
    subject_name = fields.Char(string='Subject name', related='subject_id.name')
    
    student_id = fields.Many2one('education.student', string='Student id', ondelete='restrict')
    subject_id = fields.Many2one('education.subject', string='Subjects', ondelete='restrict')
    