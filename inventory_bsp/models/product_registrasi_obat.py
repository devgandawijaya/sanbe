from odoo import models, fields, api

class ProductRegistrasiObat(models.Model):

    _name = 'product.registrasi.obat'

    name = fields.Char()  