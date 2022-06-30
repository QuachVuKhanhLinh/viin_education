from odoo import fields, models, api

class EducationClassVIP(models.Model):
    _name = 'education.class.vip'
    _description = 'Education Class VIP'
    _inherits = {'education.class': 'class_vip_id'}
    
    class_vip_id = fields.Many2one('education.class', string='Class VIP id', ondelete='restrict', required=True)
    
    sponsor_name = fields.Char(string="Sponsor name")
    contact_info = fields.Text(string='Contact Information', groups="viin_education.viin_education_group_admin")
    
    currency_id = fields.Many2one('res.currency', string="Currency Unit")
    donation = fields.Monetary(string="Amount of Money", currency_field='currency_id', default=0)
    
    total_donation = fields.Monetary(string='Total Donation',
                                     currency_field='currency_id', default=0,
                                     groups="viin_education.viin_education_group_admin")
    
    
    def donate_money(self):
        pass
    
    @api.onchange('donation')
    def onchange_donation(self):
        for record in self:
            record.total_donation += record.donation
            record.donation = 0
    
    # @api.model
    # def create(self, vals):
    #     if not 'total_donation' in vals.keys():
    #         vals['total_donation'] = 0
    #     vals['total_donation'] += vals['donation']
    #     vals['donation'] = 0
    #     records =  super(EducationClassVIP, self).create(vals)
    #     return records
    
    
    
    