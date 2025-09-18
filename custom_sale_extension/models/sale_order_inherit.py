from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    internal_reference = fields.Char(string="Internal Reference",
                                     readonly=True,
                                     groups="sales_team.group_sale_salesman_all_leads")
    has_validator_group = fields.Boolean(
        string="Show Internal Confirm Button",
        compute='_compute_show_internal_confirm_button',
        help="Controls visibility of internal confirmation button"
    )

    @api.depends()
    def _compute_show_internal_confirm_button(self):

        has_group = self.env.user.has_group('custom_sale_extension.group_internal_sales_validator')
        for order in self:
            # Show button if user has group AND order is not confirmed/cancelled AND no internal reference yet
            order.has_validator_group = has_group

    def action_internal_confirm(self):
        for order in self:
            if not order.order_line:
                raise UserError("Cannot confirm internally. Order must have at least one order line.")

            if not order.internal_reference:
                order.internal_reference = f"REF-{order.name}"
            order.env.user.notify_info(
                message=f"Internal reference {order.internal_reference} has been set!",
                title="Internal Confirmation",
                sticky=False
            )

    def action_confirm(self):
        """Override the standard confirm action to require internal confirmation first"""
        for order in self:
            if not order.internal_reference:
                raise UserError(
                    "Cannot confirm sale order. "
                    "Please complete internal confirmation first using the 'Internal confirmation' button."
                )

        # Proceed with standard confirmation (Odoo core will handle order line validation)
        return super(SaleOrderInherit, self).action_confirm()

