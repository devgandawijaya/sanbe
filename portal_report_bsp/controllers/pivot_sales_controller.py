from odoo import http
from odoo.http import request
import requests
import mysql.connector
import logging
import json
from pytz import timezone
from datetime import datetime
from requests.exceptions import ConnectionError, RequestException

_logger = logging.getLogger(__name__)

class PivotSalesController(http.Controller):
    
    @http.route('/pivot-sales-import', type='http', auth='public', csrf=False)
    def import_konsolidasi_cocba(self, **kwargs):
        konsolidasi_model = request.env['konsolidasi.master'].sudo()
        pivot_sales_model = request.env['pivot.sales'].sudo()

        konsolidasi_data = konsolidasi_model.search([])

        for record in konsolidasi_data:
            
            existing_record = pivot_sales_model.search([
                ('konsolidasi_id', '=', record.id),
                ('tgl_faktur', '=', record.tgl_faktur), 
                ('kode_barang', '=', record.kode_barang_id.id), 
                ('kode_cabang', '=', record.kode_cabang_id.id)
            ])
            if not existing_record:
                pivot_sales_model.create({
                    'konsolidasi_id': record.id,
                    'tgl_faktur': record.tgl_faktur,
                    'kode_barang': record.kode_barang_id.id,
                    'kode_cabang': record.kode_cabang_id.id,
                })
                pivot_sales_model.env.cr.commit()
        action = request.env['ir.actions.act_window'].sudo().search([('name', '=', 'Pivot Sales')], limit=1)
        action_id = action.id if action else None

        menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Pivot Sales')], limit=1)
        menu_id = menu.id if menu else None

        return request.redirect(f'/web#action={action_id}&menu_id={menu_id}')