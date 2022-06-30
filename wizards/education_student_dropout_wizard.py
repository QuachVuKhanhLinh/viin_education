from odoo import fields, models, api
from odoo.exceptions import UserError

class EducationStudentDropoutWizard(models.TransientModel):
    _name = 'education.student.dropout.wizard'
    _description = 'Education Student Dropout Wizard'

    def _default_student(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        return self.env[active_model].browse(active_id)

    student_id = fields.Many2one('education.student', string='Student', default=_default_student, required=True)
    dropout_reason = fields.Text(string='Drop-out Reason', required=True)
    student_name = fields.Char(string='Student name', related='student_id.name')
    student_code = fields.Char(string='Student code', related='student_id.student_code')
    
    def ensure_one_stage_Off(self):
        number_of_stage = self.env['education.student.stage'].search([('name', '=', 'Off')], count=True)
        if number_of_stage >1:
            raise UserError('There are two stages with the same name Off, please check again')
    
    def action_confirm(self):
        self.ensure_one_stage_Off()
        self.student_id.dropout_reason = self.dropout_reason
        self.student_id.stage_id = self.env['education.student.stage'].search([('name', '=', 'Off')])