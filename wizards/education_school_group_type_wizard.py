from odoo import models, fields, api

class EducationShoolGroupType(models.TransientModel):
    _name = 'education.school.group.type.wizard'
    
    def _default_school(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        return self.env[active_model].browse(active_id)
    
    def _default_group_type(self):
        return self._default_school().group_type
       
    school_id = fields.Many2one('education.school', string='School', default=_default_school, required=True)
    group_type = fields.Selection(string='Group Type', 
                                  selection=[('kv1', 'Khu vuc 1'), ('kv2', 'Khu vuc 2')], default=_default_group_type)
    
    def action_confirm(self):
        self.ensure_one()
        self.school_id.group_type = self.group_type