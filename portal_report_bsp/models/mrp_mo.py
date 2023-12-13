from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class mrpMo(models.Model):
    _name = 'mrp.mo'

    mo_no = fields.Char()
    mo_date = fields.Datetime()
    mo_type = fields.Char()
    mo_group = fields.Char()
    customer_code = fields.Char()
    customer = fields.Char()
    order_status = fields.Char()
    product_code = fields.Char()
    product_name = fields.Char()
    order_qty = fields.Char()
    ship_qty = fields.Char()
    pending_qty = fields.Char()
    so_no = fields.Char()
    notes = fields.Char()
    fetch_date = fields.Date()
    mop_index = fields.Integer()
    delete_after_process = fields.Boolean(default=False)

    def button_data_mo(self):
        self.ensure_one()
        self.delete_after_process = True
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "{}/mrp/mo".format(base_url)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }
    
    # Automated method for Get MRP MO Pending data 
    def cron_get_mrp_mo_per_batch(self):
        current_ext_url = "http://192.168.16.130/portal/mrp/Mrpreport/getMoPending"

        print(f'Cronjob is currently requesting data with URL: {current_ext_url}')   

        try:
            response = requests.get(current_ext_url)
            response.raise_for_status()

            if response.status_code != 200:
                print(f"External MRP MO Pending endpoint for branch Bandung didn't respond with status 200")
            else:
                print(f"MRP MO Pending data for branch Bandung successfully retrieved by cronjob")

        except requests.exceptions.RequestException as err:
            error_message = f"Error during GET request: {err}"
            print(error_message)
            _logger.error(error_message)
