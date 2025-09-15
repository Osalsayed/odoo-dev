from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    internal_reference = fields.Char(string="Internal Reference",
                                     readonly=True,
                                     groups="sales_team.group_sale_salesman_all_leads")

    def action_internal_confirm(self):
        for order in self:
            if not order.internal_reference:
                order.internal_reference = f"REF-{order.name}"
            order.env.user.notify_info(
                message=f"Internal reference {order.internal_reference} has been set!",
                title="Internal Confirmation",
                sticky=False
            )

