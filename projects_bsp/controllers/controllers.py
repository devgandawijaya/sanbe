# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectsBsp(http.Controller):
#     @http.route('/projects_bsp/projects_bsp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/projects_bsp/projects_bsp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('projects_bsp.listing', {
#             'root': '/projects_bsp/projects_bsp',
#             'objects': http.request.env['projects_bsp.projects_bsp'].search([]),
#         })

#     @http.route('/projects_bsp/projects_bsp/objects/<model("projects_bsp.projects_bsp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('projects_bsp.object', {
#             'object': obj
#         })
