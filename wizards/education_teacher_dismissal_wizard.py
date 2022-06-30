from odoo import models, fields, api

class EducationTeacherDismissalWizard(models.TransientModel):
    _name = 'education.teacher.dismissal.wizard'
    
    def _default_teacher(self):
        return self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))
    
    teacher_id = fields.Many2one('education.teacher', string='Teacher', default=_default_teacher)
    teacher_name = fields.Char(string='Teacher name', related='teacher_id.name')
    teacher_code = fields.Char(string='Teacher name', related='teacher_id.teacher_code')
    dismissal_reason = fields.Text(string='Dismissal Reason', required=True)
    
    def action_confirm(self):
        self.ensure_one()
        self.teacher_id.dismissal_reason = self.dismissal_reason
        self.teacher_id.stage_id = self.env['education.teacher.stage'].search([('name', '=', 'Retired')], limit=1)
        