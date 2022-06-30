from odoo import fields, models, api
from odoo.exceptions import UserError

class EducationClass (models.Model):
    # _name = 'educaton.class'
    _inherit = 'education.class'
    
    max_student = fields.Integer(string='maximum number of students', default=20)
    
    def add_student(self):
        if len(self.student_ids) > self.max_student:
            raise UserError("the number of students exceeds %d" % self.max_student)
        super(EducationClass, self).add_student()
        
