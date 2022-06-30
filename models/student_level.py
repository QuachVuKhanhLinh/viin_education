from odoo import fields, models, api
from odoo.exceptions import UserError

class StudentLevel(models.Model):
    _name = 'student.level'
    _description = 'Student Level'
    # _order = 'sequence, name'
    # _rec_name = 'name'
    
    name = fields.Char(string='Name', translate=True, required=True) #, default=''
    code = fields.Char(string="Code", compute="_compute_code_from_name", store=True) #, required=True
    sequence = fields.Integer(string='Sequence', default=1)
    
    # _sql_constraints = [('contains_prohibited_words', 'CHECK(name not like '"%fuck%"')', "The name contains prohibited words, please try again")]
    
    @api.constrains('name')
    def _constrains_name(self):
        prohibited_words = ['fuck', 'shit', 'god']
        for word in prohibited_words:
            for r in self:
                if word in r.name:
                    raise UserError("This name is not allowed, please choose another name")
    
    
    @api.depends('name')
    def _compute_code_from_name(self):
        for r in self:
            if isinstance(r.name, str):
                r.code = r.name.replace(' ', '-')
                