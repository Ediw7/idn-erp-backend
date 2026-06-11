{
    'name': 'EDI Accounting - Invoicing Backend',
    'version': '1.0',
    'summary': 'Headless Invoicing API for EDI Accounting System',
    'description': 'Provides REST API endpoints for React Frontend and extends res.company for Indonesian taxation.',
    'author': 'EDI Accounting System',
    'website': '',
    'category': 'Accounting/Localizations',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/setup_pelanggan_views.xml',
        'views/res_company_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
