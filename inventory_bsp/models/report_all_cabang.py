from odoo import models, fields, api


class reportallcabang(models.Model):
    _name = 'report.all.cabang'

    name = fields.Char()