from odoo import models, fields, api

class EducationSubject(models.Model):
    _name = 'education.subject'
    _description = 'Education Subject'
    
    name = fields.Char(string='Subject name', required=True)
    description = fields.Text(string='Description')
    