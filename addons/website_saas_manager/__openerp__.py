
{
    'name':  u'Saas Manager Website',
    'category': 'Website',
    'summary': u'Saas Manager Website',
    'version': '1.0',
    'description': """
Saas Manager Website
================

        """,
    'author': u'Sistemas ADHOC',
    'depends': [
        'saas_manager_x',
        'website',
        ],
    'data': [
        'views/website_product.xml',
        'security/ir.model.access.csv',
        'security/website_saas_manager.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
