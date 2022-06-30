from odoo import fields, models, api

class EducationStudentNote(models.TransientModel):
    _name = 'education.student.note.wizard'
    
    # def _default_student(self):
    #     active_model = self.env.context.get('active_model')
    #     active_id = self.env.context.get('active_id')
    #     return self.env[active_model].browse(active_id)
    #
    # student_id = fields.Many2one('education.student', string='Student', default=_default_student, required=True)
    # notes = fields.Text(string='Notes', required=True)
    #
    # def set_student_note(self):
    #     self.student_id.notes = self.notes
    
    
    def _default_student(self):
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')  
        return self.env[active_model].browse(active_ids)
    
    student_ids = fields.Many2many('education.student', string='Students', default=_default_student)
    notes = fields.Text('Notes')
    
    def set_student_note(self):
        rs= self._default_student()
        for r in rs:
            r.notes = self.notes

    