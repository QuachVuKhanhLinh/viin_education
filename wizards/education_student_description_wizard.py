from odoo import fields, models, api

class EducationStudentDescription(models.TransientModel):
    _name = 'education.student.description.wizard'
    
    def _default_student(self):
        return self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_ids'))
    
    student_ids = fields.Many2many('education.student', string='Students', required=True, default=_default_student)
    description = fields.Html(string='Description', required=True)
    
    def set_student_description(self):
        records = self._default_student()
        for record in records:
            record.description = self.description