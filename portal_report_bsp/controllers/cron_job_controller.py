from odoo import http
from odoo.http import request
from odoo import fields
from datetime import datetime, timedelta
import pytz
from . import helpers

class CronMakerController(http.Controller):

    indo_timezone = pytz.timezone('Asia/Jakarta')
    date_format = '%Y-%m-%d %H:%M:%S'

    @http.route('/create-cron/<string:model_name>', type='http', auth='public')
    def create_cron(self, model_name, **kw):
        action_name = f'Portal BSP: Get {model_name.replace("_", " ").title()} data from External Microservice'

        cron_model = request.env['ir.cron'].sudo()
        model_model = request.env['ir.model'].sudo()

        next_call_string = fields.Datetime.to_string(datetime.now(tz=self.indo_timezone) + timedelta(hours=24))
        next_call_dtime = datetime.strptime(next_call_string, self.date_format)

        # Collect the required data
        model_id = model_model.search([('name', '=', model_name.replace("_", "."))], limit=1)
        user_id = request.env.user

        # Get action_id
        ir_actions_server_id = helpers._get_action_id(action_name, model_id)
        if ir_actions_server_id:
            cron_model.create({
                'ir_actions_server_id': ir_actions_server_id.id,
                'cron_name': action_name,
                'model_id': model_id.id,
                'user_id': user_id.id,
                'interval_number': 24,
                'interval_type': 'hours',
                'active': True,
                'nextcall': next_call_dtime,
                'numbercall': 1,
                'priority': 1,
                'doall': True,
                'is_bsp_triggers': True,
                'code': f'model.cron_get_{model_name}_per_batch()'
            })
            cron_model.env.cr.commit()

        return f"Cron Job for {model_id.name} is successfully created!"
