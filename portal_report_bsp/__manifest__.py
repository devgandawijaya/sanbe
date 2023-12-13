# -*- coding: utf-8 -*-
{
    'name': "portal_report_bsp",

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
    'depends': ['base', 'inventory_bsp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/barang_datang_views.xml',
        'views/crud_server_env_views.xml',
        'views/daily_stock_views.xml',
        'views/data_dasboard_views.xml',
        'views/report_rumus_logistik_views.xml',
        'views/data_replacing_views.xml',
        'views/mrp_bpb_views.xml',
        'views/mrp_sla_views.xml',
        'views/mrp_mo_views.xml',
        'views/konsolidasi_master_views.xml',
        'views/pivot_sales_views.xml',
        'views/pivot_stock_views.xml',
        'report/data_replacing_pdf_template.xml',
        'views/ir_cron_views.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'portal_report_bsp/static/src/js/button_mrp_bpb.js',
            'portal_report_bsp/static/src/js/button_mrp_sla.js',
            'portal_report_bsp/static/src/js/button_mrp_mo.js',
            'portal_report_bsp/static/src/js/button_konsolidasi.js',
            'portal_report_bsp/static/src/js/button_replacing.js',
            'portal_report_bsp/static/src/js/button_daily_stock.js',
            'portal_report_bsp/static/src/js/button_barang_datang.js',
            'portal_report_bsp/static/src/js/button_pivot_stock.js',
            'portal_report_bsp/static/src/js/button_pivot_sale.js',
        ],
        'web.assets_qweb': [
            'portal_report_bsp/static/src/xml/button_mrp_bpb.xml',
            'portal_report_bsp/static/src/xml/button_mrp_sla.xml',
            'portal_report_bsp/static/src/xml/button_mrp_mo.xml',
            'portal_report_bsp/static/src/xml/button_konsolidasi.xml',
            'portal_report_bsp/static/src/xml/button_replacing.xml',
            'portal_report_bsp/static/src/xml/button_daily_stock.xml',
            'portal_report_bsp/static/src/xml/button_barang_datang.xml',
            'portal_report_bsp/static/src/xml/button_pivot_stock.xml',
            'portal_report_bsp/static/src/xml/button_pivot_sale.xml',
        ],
    },
}
