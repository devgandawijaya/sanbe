# -*- coding: utf-8 -*-
{
    'name': "inventory_bsp",

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
    'depends': ['base', 'sale', 'product', 'purchase', 'web', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_category.xml',
        'views/product_kelompok.xml',
        'views/product_konversi.xml',
        'views/product_ppn.xml',
        'views/product_divisi.xml',
        'views/product_ssl.xml',
        'views/product_barang.xml',
        'views/product_barang_dinkes.xml',
        'views/product_registrasi_obat.xml',
        'views/transporter_master.xml',
        'views/cabang_master.xml',
        'views/cabang_mapping.xml',
        'views/product_master.xml',
        'views/gudang_master.xml',
        'views/wilayah_kecamatan.xml',
        'views/wilayah_provinsi.xml',
        'views/wilayah_kota.xml',
        'views/wilayah_kelurahan.xml',
        'views/res_company.xml',
        # 'views/assets_backend.xml',
        'views/action_views.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_bsp/static/src/js/button_product_master.js',
            'inventory_bsp/static/src/js/button_product_konvenrsi.js',
            'inventory_bsp/static/src/js/button_product_divisi.js',
            'inventory_bsp/static/src/js/button_product_category.js',
            'inventory_bsp/static/src/js/button_cabang.js',
        ],
        'web.assets_qweb': [
            'inventory_bsp/static/src/xml/button_product_master.xml',
            'inventory_bsp/static/src/xml/button_product_konversi.xml',
            'inventory_bsp/static/src/xml/button_product_divisi.xml',
            'inventory_bsp/static/src/xml/button_product_category.xml',
            'inventory_bsp/static/src/xml/button_cabang.xml',
        ],
    },

}
