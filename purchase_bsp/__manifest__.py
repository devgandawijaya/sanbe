# -*- coding: utf-8 -*-
{
    'name': "purchase_bsp",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'views/prinsipal_channel.xml',
        'views/prinsipal_pajak.xml',
        'views/prinsipal_rekening.xml',
        'views/prinsipal_program_diskon_barang.xml',
        'views/actions.xml',
        'views/menu.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'purchase_bsp/static/src/js/button_res_partner.js',
        ],
        'web.assets_qweb': [
            'purchase_bsp/static/src/xml/button_res_partner.xml',
        ],
    },
}
