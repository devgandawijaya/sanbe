from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class mrpBpb(models.Model):
    _name = 'mrp.bpb'

    ISS_NO = fields.Char()
    ISS_DATE = fields.Date()
    ISS_STATUS = fields.Char()
    DO_NO = fields.Char()
    MO_NO = fields.Char()
    MO_TYPE = fields.Char()
    po_no = fields.Char()
    PRODUCT_CODE = fields.Char()
    PRODUCT_DESC = fields.Char()
    prod_unit = fields.Char()
    prod_group = fields.Char()
    LOT_NUMBER = fields.Char()
    iss_qty = fields.Char()
    expired_date = fields.Date()
    LOCATION_NO = fields.Char()
    CUSTOMER_CODE = fields.Char()
    CUST_NAME = fields.Char()
    exp_date = fields.Date()
    actual_date = fields.Date()
    loading_date = fields.Date()
    execdate = fields.Char()
    exp_no = fields.Char()
    exp_status = fields.Char()
    forwarder = fields.Char()
    resi_number = fields.Char()
    jumlah = fields.Char()
    total_vol = fields.Char()
    total_weight = fields.Char()
    fetch_date = fields.Date()
    bpb_index = fields.Integer()
    delete_after_process = fields.Boolean(default=False)

    def button_data_bpb(self):
        self.ensure_one()
        self.delete_after_process = True
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "{}/mrp/bpb".format(base_url)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }
    
    # Automated method for Get MRP BPB data 
    def cron_get_mrp_bpb_per_batch(self):
        current_ext_url = "http://192.168.16.130/portal/mrp/Mrpreport/getBpb"

        print(f'Cronjob is currently requesting data with URL: {current_ext_url}')   

        try:
            response = requests.get(current_ext_url)
            response.raise_for_status()

            if response.status_code != 200:
                print(f"External MRP BPB endpoint for branch Bandung didn't respond with status 200")
            else:
                print(f"MRP BPB data for branch Bandung successfully retrieved by cronjob")

        except requests.exceptions.RequestException as err:
            error_message = f"Error during GET request: {err}"
            print(error_message)
            _logger.error(error_message)