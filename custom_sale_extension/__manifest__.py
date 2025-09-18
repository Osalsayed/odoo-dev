{
    'name': 'Custom Sale Extension',
    'version': '16.0.1.0.0',
    'summary': 'Extension of Sales Order with extra fields and buttons',
    'category': 'Sales',
    'sequence': 1,
    'author': 'Osama Al-Khalifa',
    'website': '',
    'depends': ['base','sale_management'],   # dependency on sales
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/ir_sequence_data.xml',
        'report/report.xml',
        'report/report_internal_sale_confirmation.xml',
        'views/res_partner_inherit_view.xml',
        'views/sale_order_inherit_view.xml',
        'views/duplicate_quotation_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}
