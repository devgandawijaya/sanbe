from odoo import http
from odoo.http import request
import requests
# import mysql.connector
import logging
import json
import time
from pytz import timezone
from datetime import datetime
from requests.exceptions import ConnectionError, RequestException
from .constants import CABANG as list_cabang
from bigjson import FileReader
import io

_logger = logging.getLogger(__name__)

class DailyStockController(http.Controller):

    @http.route('/import-daily-stock', auth='public', method=['GET'])
    def import_daily_stock(self, **kw):
        max_attempts = 3
        attempt_delay = 5 

        action = request.env['ir.actions.act_window'].sudo().search([('name', '=', 'Daily Stock')], limit=1)
        action_id = action.id if action else None
        menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Daily Stock')], limit=1)
        menu_id = menu.id if menu else None

        for attempt in range(1, max_attempts + 1):
            try:
                url2 = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getDailyStock?kode_cabang={}"

                for branch_name, abbreviation in list_cabang.items():
                    current_int_url = url2.format(abbreviation.upper())
                    _logger.info(f"Currently importing Daily Stock data of Cabang {branch_name} to Portal BSP ERP")
                    
                    # Get from internal
                    response2 = requests.get(current_int_url)
                    response2.raise_for_status()

                    # BigJSON section
                    file_like_object = io.BytesIO(response2.content)
                    reader = FileReader(file_like_object)
                    data = reader.read()
                    data_array = data["data"]

                    # Date adjustment section
                    jakarta_tz = timezone('Asia/Jakarta')
                    current_time = datetime.now(jakarta_tz)
                    current_date_str = current_time.strftime('%Y-%m-%d')

                    # Truncate section
                    request.env.cr.execute(f"DELETE FROM daily_stock WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
                    request.env.cr.commit()
                    daily_stock_model = request.env['daily.stock'].sudo()
                    
                    # Rec logging section
                    total_records = len(data_array)
                    records_created = 0
                    
                    # Process the response from BigJSON
                    for item in data_array:
                        fetch_date = item["tanggal_penarikan_akhir"]
                        if fetch_date in ['0000-00-00', '']:
                            fetch_date = None
                        existing_daily_stock = daily_stock_model.search([
                            ('ds_index', '=', item["ds_index"]),
                            ('fetch_date', '=', fetch_date),
                            ('kode_cabang', "=", item["kode_cabang"])
                        ], limit=1)
                        if not existing_daily_stock:
                            daily_stock_model.create({
                                'kode_cabang': item["kode_cabang"],
                                'nama_cabang_id': item["nama_cabang"],
                                'kode_barang': item["kode_barang"],
                                'kode_barang_principal': item["kode_barang_principal"],
                                'group_barang': item["group_barang"],
                                'category_barang': item["category_barang"],
                                'nama_barang_id': item["nama_barang"],
                                # 'kode_principal': item.get('kode_principal"],
                                'kode_principal': item["kode_principal"],
                                'Kode_Divisi_Produk_id': item["Kode_Divisi_Produk"],
                                'jenis_barang': item["jenis_barang"],
                                'harga_terkini': item["harga_terkini"],
                                'harga_terkecil': item["harga_terkecil"],
                                'harga_terbesar': item["harga_terbesar"],
                                'qty_satuan': item["qty_satuan"],
                                'satuan_terbesar': item["satuan_terbesar"],
                                'qty_satuan_kecil': item["qty_satuan_kecil"],
                                'satuan_terkecil': item["satuan_terkecil"],
                                'qty_awal': item["qty_awal"],
                                'qty_akhir': item["qty_akhir"],
                                'tanggal_penarikan_awal': item["tanggal_penarikan_awal"] if item["tanggal_penarikan_awal"] not in ['0000-00-00', ''] else None,
                                'tanggal_penarikan_akhir': item["tanggal_penarikan_akhir"] if item["tanggal_penarikan_akhir"] not in ['0000-00-00', ''] else None,
                                'fetch_date': item["tanggal_penarikan_akhir"] if item["tanggal_penarikan_akhir"] not in ['0000-00-00', ''] else None,
                                'tgl_stock': item["tgl_stock"] if item["tgl_stock"] not in ['0000-00-00', ''] else None,
                                'rev_ssl': item["rev_ssl"],
                                'avail_akhir': item["avail_akhir"],
                                'ds_index': item["ds_index"]
                            })
                            records_created += 1
                            daily_stock_model.env.cr.commit()
                            _logger.info(f"Total Daily Stock {records_created} data created of total {total_records} data in Cabang {branch_name}.")

                return request.redirect(f'/web#action={action_id}&menu_id={menu_id}')

            except requests.exceptions.RequestException as e:
                if attempt < max_attempts:
                    _logger.info(f"Attempt {attempt} failed. Retrying in {attempt_delay} seconds.")
                    time.sleep(attempt_delay)
                else:
                    return json.dumps({'error': str(e)})
