from odoo import fields, models, api


class EducationStudentCopy(models.Model):
   _name = 'education.student.copy'
   _inherits = {'res.partner': 'partner_id'}
   _description = 'Education Student - Copy'

   partner_id = fields.Many2one('res.partner', string='Student', ondelete="restrict", required=True)
   date_of_birth = fields.Date(string='Date of Birth')
   age = fields.Integer(string='Age')
   
