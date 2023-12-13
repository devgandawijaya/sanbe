from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class mrpSla(models.Model):
    _name = 'mrp.sla'

    productOwner = fields.Char()
    ProductionUnit = fields.Char()
    ProductCode = fields.Char()
    ProductName = fields.Char()
    UOMCodeDefault = fields.Char()
    ProductCategory = fields.Char()
    MonthlyForecastQuantity = fields.Char()
    MORequest = fields.Char()
    MODelivery = fields.Char()
    MOPendingQuantity = fields.Char()
    WIPBalanceQty = fields.Char()
    QuarantinedBalanceQuantity = fields.Char()
    QuarantinedHoldBalanceQuantity = fields.Char()
    QuarantinedLastLotNo = fields.Char()
    ReleasedBalanceQuantity = fields.Char()
    ReleasedBalanceHoldQuantity = fields.Char()
    ReleasedBalanceAndHoldQuantity = fields.Char()
    ReleasedLastLotNo = fields.Char()
    TotalStockQuantity = fields.Char()
    LevelTotalValuemonths = fields.Char()
    ReadyStockQuantity = fields.Char()
    LevelReadyValuemonths = fields.Char()
    PlantGroup = fields.Char()
    exeuid = fields.Char()
    exetime = fields.Datetime()
    fetch_date = fields.Date()
    sla_index = fields.Integer()
    delete_after_process = fields.Boolean(default=False)

    def button_data_sla(self):
        self.ensure_one()
        self.delete_after_process = True
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "{}/mrp/sla".format(base_url)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }
    
    # Automated method for Get MRP SLA data 
    def cron_get_mrp_sla_per_batch(self):
        current_ext_url = "http://192.168.16.130/portal/mrp/Mrpreport/getSla"

        print(f'Cronjob is currently requesting data with URL: {current_ext_url}')   

        try:
            response = requests.get(current_ext_url)
            response.raise_for_status()

            if response.status_code != 200:
                print(f"External MRP SLA endpoint for branch Bandung didn't respond with status 200")
            else:
                print(f"MRP SLA data for branch Bandung successfully retrieved by cronjob")

        except requests.exceptions.RequestException as err:
            error_message = f"Error during GET request: {err}"
            print(error_message)
            _logger.error(error_message)