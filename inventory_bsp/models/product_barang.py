from odoo import models, fields, api

class ProductBarang(models.Model):

    _name = 'product.barang'

    name = fields.Char()  