from odoo import fields, models, api
from odoo.addons.test_convert.tests.test_env import record
from odoo.fields import Datetime
from odoo.modules import get_resource_path
import base64

class EducationSchool(models.Model):
    _name = 'education.school'
    _description = 'School'
    
    name = fields.Char(string='Name', translate=True, required=True)
    avatar = fields.Binary(string='Avatar', attachment=True)
    code = fields.Char(string='Code', copy=False)
    financial_type = fields.Selection(string="Financial Type", 
                                      groups="viin_education.viin_education_group_admin",
                                      selection=[('public', 'Cong lap'), ('private', 'Dan lap')], default='public')
    
    address = fields.Text(string='Address', copy=False)
    established_date = fields.Date(string="Established Date", required=True, default=fields.Date.today)
    years_old_compute = fields.Integer(string='years old', compute='_compute_years_old', default=0, store=True)
    location = fields.Selection(string="Location", selection=[('northern', 'Mien Bac'),
                                                              ('central', 'Mien Trung'),
                                                              ('southern', 'Mien Nam')], default='northern')
    
    group_type = fields.Selection(string='Group Type', selection=[('kv1', 'Khu vuc 1'), ('kv2', 'Khu vuc 2')], default='kv1')
    plus_scrore = fields.Float(string='Plus Score', default=0, digits=(12,2), readonly=True, compute='_compute_plus_score')
    rank = fields.Integer(string="Rank", groups="viin_education.viin_education_group_admin")
    
    class_ids = fields.One2many('education.class', 'school_id', string='Classes')
    teacher_ids = fields.One2many('education.teacher','school_id',string='Teachers')
    
    class_count = fields.Integer(string='Class Count', compute='_compute_counting_class')
    teacher_count = fields.Integer(string='Teacher Count', compute='_compute_counting_teacher')
    
    def _compute_counting_class(self):
        self.class_count = len(self.class_ids)
    
    def _compute_counting_teacher(self):
        self.teacher_count = len(self.teacher_ids)
        
    def del_schools_have_no_code(self):
        schools = self.env['education.school'].search([], order='id')
        for school in schools:
            if not school.code:
                super(EducationSchool, school).unlink()
        return True
    
    displayed_time = fields.Char(string="Display time", compute="_compute_time")
    
    @api.depends('established_date')
    def _compute_time(self):
        self.displayed_time = fields.Datetime.now().strftime("%H:%M:%S")
        return self.displayed_time
    
    @api.depends('established_date')
    def _compute_years_old(self):
        current_year = fields.Date.today().year
        for r in self:
            if r.established_date:
                r.years_old_compute = current_year - r.established_date.year
            else:
                r.years_old_compute = 0
    
    @api.depends('group_type')
    def _compute_plus_score(self):
        for r in self:
            if r.group_type == 'kv1':
                r.plus_scrore = 1
            elif r.group_type == 'kv2':
                r.plus_scrore = 2
            else:
                r.plus_scrore = 0
    
    @api.model
    def create_school(self, vals):
        school_01 = {'name': 'auto-generated school 01'}
        school_02 = {'name': 'auto-generated school 02'}
        vals = [school_01,school_02]
        
        records = super(EducationSchool, self).create(vals)
        return records
    
    # thuc hanh filter()
    def show_schools_in_location(self, str_location):
        schools = self.env['education.school'].search([])
        filtered_schools = schools.filtered(lambda school: school.location == str_location)
        
        print(filtered_schools)
        return filtered_schools
    
    def show_schools_in_location_northern(self):
        self.show_schools_in_location('northern')
        
    def show_schools_in_location_central(self):
        self.show_schools_in_location('central')
        
    def show_schools_in_location_southern(self):
        self.show_schools_in_location('southern')
    
    #thuc hanh map()
    def show_school_names(self):
        schools = self.env['education.school'].search([])
        records = schools.mapped('name')
        return records
    
    def show_classes_in_school(self):
        classes = self.mapped('class_ids')
        return classes
    
    def group_by_location(self):
        group_result = self.read_group(domain=[], 
                                       fields=['name,code,financial_type'], 
                                       groupby=['location'], 
                                       offset=0, limit=None, orderby=False, lazy=False)
        
        for r in group_result:
            print(r.items())
        return group_result
    
    def show_all_public_and_private_schools_accessright_admin(self):
        education_group_admin = self.env.ref('viin_education.viin_education_group_admin')
        schools = self.env['education.school'].with_user(education_group_admin).search([])
        
        return schools

    @api.model
    def default_get(self, fields_list):
        res = super(EducationSchool, self).default_get(fields_list)
        try:
            path = get_resource_path('viin_education', 'static/src/img', 'default_school.png')
            res['avatar'] = base64.b64encode(open(path, 'rb').read()) if path else False
        except (IOError, OSError):
            res['avatar'] = False
        return res
    
    def action_group_type(self):
        return self.env.ref('viin_education.education_school_group_type_wizard_action').read()[0]
        
    
    
    
    
    
    
    
    