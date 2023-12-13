from odoo import models, fields, api


class cabangMaster(models.Model):
    _name = 'cabang.mapping'

    name = fields.Char()