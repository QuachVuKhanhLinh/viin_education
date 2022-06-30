from odoo import fields, models, api
from odoo.exceptions import ValidationError
import odoo
import base64

class ChangePasswordUser(models.TransientModel):
    _inherit = 'change.password.user'

    teacher_ids = fields.One2many('education.teacher', 'user_id', string='Teacher id')
     
    def change_password_button(self):
        self.env['education.teacher'].search([('user_id', '=', self.user_id.id)]).password = self.new_passwd
        super(ChangePasswordUser, self).change_password_button()
        
        

class EducationTeacher(models.Model):
    _name = 'education.teacher'
    _description = 'Education teacher'
    
    name = fields.Char(string='Full name')
    first_name = fields.Char(string='First name')
    last_name = fields.Char(string='Last name')
    active = fields.Boolean(string='Active', invisible=True, default=True)
    avatar = fields.Binary(string='Avatar', attachment=True)
    teacher_code = fields.Char(string='Teacher Code', required=True)
    living_area = fields.Selection(string="Living Area", selection=[('northern', 'MIEN BAC'), ('central', 'MIEN TRUNG'), ('southern', 'MIEN NAM')], default='northern')
    class_ids = fields.Many2many(comodel_name='education.class', relation='rel_student_teacher', domain="[('school_id', '=', school_id)]")
    school_id = fields.Many2one('education.school', string='School')
    description = fields.Html(string="Description", sanitize=True)
    images = fields.Image(string="images", max_width=128, max_height=128)
    english_level = fields.Selection(string='English Level', selection=[('basic', 'BASIC'), ('intermediate', 'INTERMEDIATE'), ('advanced', 'ADVANCE')], default='basic')
    start_working_date = fields.Date(string='Start working date', default=fields.Date.today)
    years_of_working = fields.Integer(string="Years of working", compute="_compute_years_of_working", default=0, readonly=True, store=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    salary = fields.Monetary(string="Salary", currency_field='currency_id', groups="viin_education.viin_education_group_admin")
    bonus = fields.Monetary(string="bonus", currency_field='currency_id', compute='_compute_bonus', readonly=True, store=True)
    class_count = fields.Integer(string="Class Count", compute='_compute_counting_teachers')
    dismissal_reason = fields.Text(string='Dismissal Reason', readonly=True)
    user_id = fields.Many2one('res.users', string='Login Account', ondelete='restrict')
    password = fields.Char(help="Keep empty if you don't want the user to be able to connect on the system.", readonly=True)
    confirmed_password = fields.Char(string='Confirm the password', store=False)
    
    
    def _default_stage_id(self):
        return self.env['education.teacher.stage'].search([], limit=1)
    stage_id = fields.Many2one('education.teacher.stage', string='Stage', default=_default_stage_id, group_expand='_group_expand')
            
    _sql_constraints = [('teacher_code_unique', 'unique(teacher_code)', "the teacher's code must be unique!"),
                        ('check_salary', 'CHECK(salary >=0)', "The salary must be greater than or equal to 0")]
    
    @api.model
    def default_get(self, fields_list):
        res = super(EducationTeacher, self).default_get(fields_list)
        try:
            path = odoo.modules.get_resource_path('viin_education', 'static/src/img', 'default_teacher.png')
            res['avatar'] = base64.b64encode(open(path, 'rb').read()) if path else False
        except (IOError, OSError):
            res['avatar'] = False
        return res
    
    def _compute_counting_teachers(self):
        self.class_count = len(self.class_ids)
    
    @api.depends('start_working_date')
    def _compute_years_of_working(self):
        current_year = fields.Date.today().year
        for r in self:
            if r.start_working_date:
                r.years_of_working = current_year - r.start_working_date.year
            else:
                r.years_of_working = 0
    
    @api.depends('english_level', 'years_of_working')
    def _compute_bonus(self):
        for r in self:
            if r.english_level == 'basic' and r.years_of_working >= 2:
                r.bonus = 0
            elif r.english_level == 'intermediate' and r.years_of_working >= 2:
                r.bonus = 2000 * r.years_of_working
            elif r.english_level == 'advanced' and r.years_of_working >= 2:
                r.bonus = 4000 * r.years_of_working
    
    '''
    years_of_working <= 5 thi luong khong duoc >=50000
    '''
    @api.constrains('years_of_working', 'salary')
    def _check_salary_depended_years_of_working(self):
        for r in self:
            if r.years_of_working <= 5 and r.salary >= 50000:
                raise ValidationError('The salary for teacher who have less than or equal to 5 years of experience is not allowed to greater than 50000')
    
    '''
    giao vien nghi huu thi luong = 0, bonus = 0, description = retired
    ''' 
    @api.constrains('start_working_date')
    def _check_start_working_date(self):
        for r in self:
            if r.start_working_date > fields.Date.today():
                raise ValidationError("the start working date must be today or in the pass!")
    
    @api.model
    def create(self, vals):
       '''
       input first name + last name ==> full name
       '''
       vals['name'] = vals['first_name'] + " " + vals['last_name']
       
       records = super(EducationTeacher, self).create(vals)
       return records
    
    def create_teacher(self):
        teacher_01 = {
            'name': 'auto-generated teacher',
            'teacher_code': 'x', # teacher_code must be unique
            'school_id': ''
            }
        
        records = super(EducationTeacher, self).create(teacher_01)
        return records

    def unlink_auto_generated_teacher(self):
        for r in self:
            if r.teacher_code == 'x':
                super(EducationTeacher,r).unlink()
            return True
               
    def update_retired_teacher(self):
        teachers = self.env['education.teacher'].search([], limit=999, order="id")
        vals = {
            'salary': 0,
            'bonus': 0,
            'description': 'this one has already retired'
        }
        
        for r in teachers:
            if r.state == 'retired':
                super(EducationTeacher,r).write(vals)
        return True
    
    def change_into_probation(self):
        self.ensure_one()
        self.state = 'probation'
        
    def change_into_teaching(self):
        self.ensure_one()
        self.state = 'teaching'
        
    def change_into_retired(self):
        self.ensure_one()
        self.state = 'retired'
    
    def get_all_teacher(self):
        return self.search([])
    
    def get_teacher_retired_search(self):
        domain = [('state', '=', 'retired')]
        teachers = self.search(domain)
        
        print(teachers)
        return teachers
    
    def get_teacher_reired_filter(self):
        teachers = self.env['education.teacher'].search([])
        
        # filtered_teachers= teachers.filtered_domain([('state', '=', 'retired')])
        filtered_teachers = teachers.filtered(lambda teacher: teacher.state == 'retired')   #note 3
        return filtered_teachers
    
    def get_teacher_retired_map(self):
        teachers = self.env['education.teacher'].search([])
        
        #return list of teachers name
        return teachers.mapped('name')
    
    def group_teacher_by_living_area(self):
        group_result = self.read_group(
           [('state', '=', 'teaching')],
           ['living_area'],
           ['living_area']
           )
        print(group_result)
        return group_result
    

    @api.model
    def _group_expand(self, stages, domain, order):
        return stages.search([], order=order)
    
    def action_dismissal(self):
        return self.env.ref('viin_education.education_teacher_dismissal_wizard_action').read()[0]
    
    
    
    
        
    
    
    
    
    
    
    
    
    