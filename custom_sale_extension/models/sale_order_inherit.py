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

            if not self.env.context.get('force_internal_confirm', False):
                duplicate = order._check_duplicate_quotation()
                if duplicate:
                    return {
                        'name': 'Duplicate Quotation Found',
                        'type': 'ir.actions.act_window',
                        'res_model': 'duplicate.quotation.wizard',
                        'view_mode': 'form',
                        'target': 'new',
                        'context': {
                            'dialog_size': 'extra-large',
                            'default_order_id': order.id,
                            'default_duplicate_order_id': duplicate.id,
                        }
                    }

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

    def _check_duplicate_quotation(self):
        """Check for duplicates: same customer + exact same set of products"""
        for order in self:
            product_ids = set(order.order_line.mapped('product_id.id'))
            if not product_ids:
                continue

            # Search all other quotations for this customer
            duplicates = self.search([
                ('id', '!=', order.id),
                ('partner_id', '=', order.partner_id.id),
                ('state', 'in', ['draft', 'sent']),
            ])

            for dup in duplicates:
                dup_products = set(dup.order_line.mapped('product_id.id'))
                if dup_products == product_ids:
                    return dup  # Exact match found

        return False


