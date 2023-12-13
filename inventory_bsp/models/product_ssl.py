from odoo import models, fields, api

class ProductSsl(models.Model):

    _name = 'product.ssl'

    name = fields.Char()  