from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(string="Customer Code",
                                readonly=True,
                                store=True,
                                copy=False,
                                index=True,
                                groups="sales_team.group_sale_salesman_all_leads")

    creation_order = fields.Char(
        string="Creation Order",
        compute="_compute_creation_order",
        store=False,  # not stored, recomputed every time
        readonly=True
    )

    @api.depends('create_date')
    def _compute_creation_order(self):
        Partner = self.with_context(active_test=False)
        for partner in self:
            if not partner.create_date:
                partner.creation_order = False
                continue
            count_older_or_equal = Partner.search_count([
                '&',
                ('create_date', '<=', partner.create_date),  # Same or older
                ('id', '<=', partner.id),  # Tie-breaker
            ])
            # count already includes this partner because of <=
            partner.creation_order = f"CRE{count_older_or_equal:03d}"

    @api.model
    def create(self, vals):
        if not vals.get('customer_code'):
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('res.partner.customer.code')
        return super(ResPartnerInherit, self).create(vals)
