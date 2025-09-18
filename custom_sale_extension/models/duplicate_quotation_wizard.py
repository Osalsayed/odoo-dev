from odoo import models, fields


class DuplicateQuotationWizard(models.TransientModel):
    _name = 'duplicate.quotation.wizard'
    _description = 'Duplicate Quotation Warning'

    order_id = fields.Many2one('sale.order', string="Current Quotation")
    duplicate_order_id = fields.Many2one('sale.order', string="Duplicate Quotation")

    def action_view_duplicate(self):
        return {
            'name': 'Duplicate Quotation',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.duplicate_order_id.id,
        }

    def action_confirm_anyway(self):
        self.order_id.with_context(force_internal_confirm=True).action_internal_confirm()
        return {'type': 'ir.actions.act_window_close'}
