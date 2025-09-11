from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(string="Customer Code", readonly=True,store=True, copy=False, index=True, unique=True,search=True)

    @api.model
    def create(self, vals):
        if not vals.get('customer_code'):
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('res.partner.customer.code')
        return super(ResPartnerInherit, self).create(vals)
