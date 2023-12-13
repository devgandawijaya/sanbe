from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)



class CrudServerEnv(models.Model):
    _name = 'crud.server.env'

    cabang_master_id = fields.Many2one('res.company', 'Name Cabang Master')
    ip = fields.Char('IP')
    port = fields.Char('PORT')
    username = fields.Char('Username')
    password = fields.Char('Password')
    status = fields.Selection([('activate', 'Activate'), ('deactivate', 'Deactivate')])
    database_name = fields.Char()
