from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CronJobsBSP(models.Model):
    _inherit = 'ir.cron'

    is_bsp_triggers = fields.Boolean(string="Is BSP Cron Job", default=False)