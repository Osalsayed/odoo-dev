from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    internal_reference = fields.Char(string="Internal Reference", readonly=True)

    def action_internal_confirm(self):
        """Custom button: generate internal reference"""
        for order in self:
            if not order.internal_reference:
                order.internal_reference = f"REF-{order.name}"
            order.env.user.notify_info(
                message=f"Internal reference {order.internal_reference} has been set!",
                title="Internal Confirmation",
                sticky=False  # True if you want it to stay
            )