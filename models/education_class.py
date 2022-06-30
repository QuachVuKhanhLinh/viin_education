from odoo import fields, models, api

class EducationClass(models.Model):
    _name = 'education.class'
    _description = 'Education Class'
    # _inherit = 'base.education'
    
    name = fields.Char(string="Name", required=True)
    school_id = fields.Many2one('education.school', string='School', required=True)
    # class_group_id = fields.Many2one('education.class.group', string="class group")
    
    student_ids = fields.One2many('education.student', 'class_id', string='Students', domain="[('school_id', '=', school_id)]")    
    teacher_ids = fields.Many2many(comodel_name='education.teacher', relation='rel_student_teacher', domain="[('school_id', '=', school_id)]")
    
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')
    
    def _compute_student_count(self):
        self.student_count = len(self.student_ids)
    
    def change_class_name(self):
        self.ensure_one()
        self.write({
            'name': 'VIP'
            })
        
    @api.model
    def create_classes(self, vals):
        student_01 = {
            'name': 'student auto-generated 01'
            }
        student_02 = {
            'name': 'student auto-generated 02'
            }
        class_01 = {
            'name': 'class auto-generated 01',
            'student_ids': [
                (0,0,student_01),
                (0,0,student_02)
                ],
            'school_id' : 1
            }
        
        vals = [class_01]
        records = super(EducationClass, self).create(vals)
        return records
    
    def get_all_students(self):
        student = self.env['education.student']
        all_students = student.search([])
        for student in all_students:
            print(student.name)
            
        return all_students    
        
    def get_all_class_name(self):
        all_cla = self.env['education.class'].search([])
        for cla in all_cla:
            print(cla.name)
            
        return all_cla
        
    # loc lop co nhieu hon hoac bang 1 hoc sinh   
    def classes_has_student(self):
        classes = self.env['education.class'].search([])
        print(classes)
        classes.filtered(lambda c: len(c.student_ids) >= 1)
        print(classes)

        # filtered_classes = filter(lambda c: len(c.student_ids) >=1, all_classes)
    

    # lay ten hoc sinh tu mot recordset lop hoc
    
    def get_student_names(self):
        students = self.env['education.student'].search([])
        return print(students.mapped('name'))
    
    dob = fields.Date(string="Date of birth")
    
    @api.model
    def sort_students_by_dob(self, students):
        sorted_students = sorted(students, reverse=True)
        print(sorted_students)
        return sorted_students
    
    def add_student(self):
        self.ensure_one()
        self.write({
            'student_ids': [(0, 0, {
                'name': 'auto-generated class'
            })]
        })
    
        
        
        
        