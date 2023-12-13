# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseBsp(http.Controller):
#     @http.route('/purchase_bsp/purchase_bsp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_bsp/purchase_bsp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_bsp.listing', {
#             'root': '/purchase_bsp/purchase_bsp',
#             'objects': http.request.env['purchase_bsp.purchase_bsp'].search([]),
#         })

#     @http.route('/purchase_bsp/purchase_bsp/objects/<model("purchase_bsp.purchase_bsp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_bsp.object', {
#             'object': obj
#         })
