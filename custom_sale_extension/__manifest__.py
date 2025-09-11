{
    'name': 'Custom Sale Extension',
    'version': '16.0.1.0.0',
    'summary': 'Extension of Sales Order with extra fields and buttons',
    'category': 'Sales',
    'author': 'Osama Al-Khalifa',
    'website': '',
    'depends': ['base','sale_management'],   # dependency on sales
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/res_partner_inherit_view.xml',
        'views/sale_order_inherit_view.xml',
    ],
    'installable': True,
    'application': False,
}
