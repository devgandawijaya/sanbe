# -*- coding: utf-8 -*-
# from odoo import http


# class PortalReportBsp(http.Controller):
#     @http.route('/portal_report_bsp/portal_report_bsp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/portal_report_bsp/portal_report_bsp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('portal_report_bsp.listing', {
#             'root': '/portal_report_bsp/portal_report_bsp',
#             'objects': http.request.env['portal_report_bsp.portal_report_bsp'].search([]),
#         })

#     @http.route('/portal_report_bsp/portal_report_bsp/objects/<model("portal_report_bsp.portal_report_bsp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('portal_report_bsp.object', {
#             'object': obj
#         })
