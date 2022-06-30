from odoo import fields, models, api
from odoo.exceptions import UserError

class TeacherLevel(models.Model):
    _name = 'teacher.level'
    _description = 'Teacher level'
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", readonly="True", compute="_compute_code_from_name", store=True)
    
    @api.constrains('name')
    def _check_name(self):
        prohibited_characters = ['!', '@', '#', '$', '%']
        for character in prohibited_characters:
            for r in self:
                if character in r.name:
                    raise UserError('contains prohibited characters, please choose another name!')
    
    @api.depends('name')
    def _compute_code_from_name(self):
        for r in self:
            if isinstance(r.name, str):
                r.code = r.name.replace(' ', '-')