from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from passlib.tests.utils import limit
import odoo
import base64


class EducationStudent(models.Model):
   _name = 'education.student'
   _description = 'Education Student'
   _order = 'student_code desc'
   _rec_name = 'student_code'
   
   name = fields.Char(string='Student Name', select=True, help='Enter your name', translate=True)
   first_name = fields.Char(string='First name', required=True)
   last_name = fields.Char(string='Last name', required=True)
   active = fields.Boolean(string='Active', help="nothing to help", default=True) 
   student_code = fields.Char(string='Student Code', index=True, copy=False)
   gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', default='male')
   date_of_birth = fields.Date(string='Date of Birth', default=fields.Date.today)
   notes = fields.Text(string='Internal Notes')  # readonly=True
   description = fields.Html(string='Description', sanitize=True, strip_style=False)
   avatar = fields.Binary(string='Avatar', attachment=True, prefetch=False)
   images = fields.Image(string='Images', max_width=1980 / 8, max_height=1080 / 8)
   dropout_reason = fields.Text(string='Dropout Reason')
   write_date = fields.Datetime(string='Last Updated on', readonly=True)
   currency_id = fields.Many2one('res.currency', string='Currency')
   amount_paid = fields.Monetary('Amount Paid', currency_field='currency_id')
   school_id = fields.Many2one('education.school', string="School")
   class_id = fields.Many2one('education.class', string='Class', domain="[('school_id', '=', school_id)]")
   school_code = fields.Char(related='school_id.code', string="School code")
   school_address = fields.Text(related='school_id.address', string='School Address')
   age = fields.Integer(string='Age', compute='_compute_age', inverse='_inverse_age', search='_search_age', store=False)
   def _default_stage_id(self):
       return self.env['education.student.stage'].search([], limit=1)
   stage_id = fields.Many2one('education.student.stage', string="Stage", default=_default_stage_id, group_expand='_group_expand')
   score_ids = fields.One2many('education.student.score', 'student_id', string='Scores')
   average_score = fields.Float(string="Average score", digits=(12,2), default=0, compute='_compute_average_score')
   
   
   _sql_constraints = [('student_code_unique', 'unique(student_code)', "The student code must be unique!")] #('check_total_score', 'CHECK(total_score >= 0)', "The Total Score must be greater than 0!")
   
   
   @api.model
   def default_get(self, fields_list):
       res = super(EducationStudent, self).default_get(fields_list)
       try:
           path = odoo.modules.get_resource_path('viin_education', 'static/src/img', 'default_student.png')
           res['avatar'] = base64.b64encode(open(path, 'rb').read()) if path else False
       except (IOError, OSError):
           res['avatar'] = False
       return res  
   
   def _search_age(self, operator, value):
         new_year = fields.Date.today().year - value
         new_value = fields.date(new_year, 1, 1)
         # age > value => date_of_birth < new_value
         operator_map = {'>': '<', '>=': '<=', '<': '>', '<=': '>='}
         new_operator = operator_map.get(operator, operator)
         return [('date_of_birth', new_operator, new_value)]
   
   @api.depends('date_of_birth')
   def _compute_age(self):
       current_year = fields.Date.today().year
       for r in self:
           if r.date_of_birth:
               r.age = current_year - r.date_of_birth.year
           else:
               r.age = 0
   
   def _compute_average_score(self):
       total = (0.0)
       scores = self.env['education.student.score'].search([]).mapped('score')
       for score in scores:
           total += score
       self.average_score = total/len(scores)
   
   
   @api.constrains('date_of_birth')
   def _check_date_of_birth(self):
       for r in self:
           if r.date_of_birth > fields.Date.today():
               raise ValidationError('date of birth must be in the past')
   

   @api.model
   def create(self, vals):
       '''
       input first name + last name ==> full name
       '''
       vals['name'] = vals['first_name'] + " " + vals['last_name']
       
       records = super(EducationStudent, self).create(vals)
       return records
   
   def write_note_for_vip_students(self):
       '''
       write note for v.i.p students
       '''
       domain = [('class_id', 'ilike', 'VIP')]
       students = self.env['education.student'].search(domain)
       vals = {'notes': 'this is VIP student, must care much more about them'}
       for student in students:
           super(EducationStudent, student).write(vals) 
       return True
   
   def unlink_students_have_no_school_id(self):
       '''
       delete students don't have school_id
       '''
       students = self.search([('school_id', '=', False)])
       for student in students:
           student.unlink()    
   
   def action_dropout(self):
       return self.env.ref('viin_education.education_student_dropout_wizard_action').read()[0]
   
   
   @api.model
   def _group_expand(self, stages, domain, order):
       return stages.search([], order=order)
   
   @api.model
   def is_allowed_state(self, current_state, new_state):
       allowed_state = [('new', 'studying'), ('studying', 'off'), ('off', 'studying'), ('new', 'off')]
       return (current_state, new_state) in allowed_state
   
   def change_student_state(self, state):
       for student in self:
           if student.is_allowed_state(student.state, state):
               student.state = state
           else:
               raise UserError("Changing state from %s to %s is not allowed" % (student.state, state))
    
   def change_to_new(self):
       self.change_student_state('new')
       
   def change_to_studying(self):
       self.change_student_state('studying')
       
   def change_to_off(self): 
       self.change_student_state('off')
   
   def search_student(self, string_gender):
        students = self.env['education.student'].search([('gender', '=', string_gender)], limit=5, order='student_code')  
        print(students)

   def search_gender_male(self):
       self.search_student('male')
       
   def search_gender_female(self):
       self.search_student('female')
       
       
   def _inverse_age(self):
       for r in self:
           if r.age and r.date_of_birth:
               current_year = fields.Date.today().year
               dob_year = current_year - r.age
               dob_month = r.date_of_birth.month
               dob_day = r.date_of_birth.day
               date_of_birth = fields.date(dob_year, dob_month, dob_day)
   
               r.date_of_birth = date_of_birth
               
   def find_VIP_student(self):
       domain = ['|', ('name', 'ilike', 'VIP'), ('class_id.name', '=', 'VIP')]
       students = self.search(domain)
       for student in students:
           print(student)
       return students

   def get_student_has_no_class(self):
       domain = [('class_id', '=', False)]
       students = self.env['education.student'].search(domain)
       print(students)
       return students
   
   def group_students_by_school(self):
       group_result = self.read_group(
           domain=[], #('stage_id', '=', 'new')
           fields=['name', 'stage_id', 'class_id', 'school_id'],
           groupby=['school_id', 'gender'],
           )

       return group_result

   @api.model
   def _update_student_code(self):
       all_students = self.search([])
       for student in all_students:
           student.student_code = '%s_%s' % (student.school_id.code, student.student_code)
   
   def show_all_public_and_private_schools_accessright_admin(self):
       education_group_admin = self.env.ref('base.user_admin')
       schools = self.env['education.school'].with_user(education_group_admin).search([])
        
       return schools
   
   
   
