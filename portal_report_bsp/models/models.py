# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class portal_report_bsp(models.Model):
#     _name = 'portal_report_bsp.portal_report_bsp'
#     _description = 'portal_report_bsp.portal_report_bsp'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
