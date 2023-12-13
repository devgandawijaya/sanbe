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

class BarangDatangController(http.Controller):
    
    @http.route('/import-barang-datang', auth='public', method=['GET'])
    def import_barang_datang(self, **kw):
        max_attempts = 3
        attempt_delay = 5 

        action = request.env['ir.actions.act_window'].sudo().search([('name', '=', 'Barang Datang')], limit=1)
        action_id = action.id if action else None
        menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Barang Datang')], limit=1)
        menu_id = menu.id if menu else None

        for attempt in range(1, max_attempts + 1):
            try:
                url2 = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getBarangDatang/?kode_cabang={}"            
                
                for branch_name, abbreviation in list_cabang.items():
                    current_int_url = url2.format(abbreviation.upper())
                    _logger.info(f"Currently importing Barang Datang data of Cabang {branch_name} to Portal BSP ERP")
                
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
                    request.env.cr.execute(f"DELETE FROM barang_datang WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
                    request.env.cr.commit()
                    barang_datang_model = request.env['barang.datang'].sudo()
                    
                    # Rec logging section
                    total_records = len(data_array)
                    records_created = 0
                    
                    # Process the response from BigJSON
                    for item in data_array:
                        fetch_date = item["fetch_date"]
                        if fetch_date in ['0000-00-00', '']:
                            fetch_date = None
                        existing_barang_datang = barang_datang_model.search([
                            ('bd_index', '=', item["bd_index"]),
                            ('fetch_date', '=', fetch_date),
                            ('kode_cabang', "=", item["kode_cabang"])
                        ],limit=1)
                        kode_barang = request.env['product.template'].search([
                            ('kode_barang', '=', item["kode_barang"])
                        ], limit=1)
                        # if not kode_barang:
                        #     kode_barang = request.env['product.template'].with_context(skip_external_api=True).create({
                        #         'name': item.get('nama_barang'),  # Using the nama_barang as the name for the new product.template
                        #         'kode_barang': item.get('kode_barang')  # Setting the kode_barang for the new record
                        #         })

                        nama_cabang = request.env['res.company'].search([
                                ('name', '=', item["nama_cabang"])
                            ], limit=1)
                        kode_divisi = request.env['product.divisi'].search([
                                ('kode_divisi_produk', '=', item["kode_divisi_produk"])
                            ], limit=1)
                        kode_prinsipal = item["kode_principal"]
                        if kode_prinsipal:
                            partner = request.env['res.partner'].search([('kode_principal', '=', kode_prinsipal)], limit=1)
                            partner_id = partner.id if partner else False
                        else:
                            partner_id = False
                        if not existing_barang_datang:
                            barang_datang_model.create({
                                'kode_cabang': item["kode_cabang"],
                                'nama_cabang_id': nama_cabang.id if nama_cabang else False,
                                'no_barang_datang': item["no_barang_datang"],
                                'tgl_bd': item["tgl_bd"],
                                'tgl_po': item["tgl_po"],
                                'no_surat_jalan': item["no_surat_jalan"],
                                'no_bpb': item["no_bpb"],
                                'no_spb': item["no_spb"],
                                'no_do': item["no_do"],
                                'no_po': item["no_po"],
                                'tglpajak': item["tglpajak"],
                                'nopajak': item["nopajak"],
                                'topfkt': item["topfkt"],
                                'jenis_faktur': item["jenis_faktur"],
                                'jenis_beli': item["jenis_beli"],
                                'jenis_mac': item["jenis_mac"],
                                'sub_jenis_beli': item["sub_jenis_beli"],
                                'pcpl_kode': item["pcpl_kode"],
                                'noitem': item["noitem"],
                                'kode_barang_id': kode_barang.id if kode_barang else False,
                                'kode_barang_bis': item["kode_barang_bis"],
                                'nama_barang': item["nama_barang"],
                                'nobatch': item["nobatch"],
                                'qty_transaksi': item["qty_transaksi"],
                                'satuan_transaksi': item["satuan_transaksi"],
                                'harga_transaksi': item["harga_transaksi"],
                                'qty_beli_terkecil': item["qty_beli_terkecil"],
                                'harga_beli_terkecil': item["harga_beli_terkecil"],
                                'satuan_beli_terkecil': item["satuan_beli_terkecil"],
                                'ssl_pr': item["ssl_pr"],
                                'qty_order_terkecil': item["qty_order_terkecil"],
                                'satuan_order_terkecil': item["satuan_order_terkecil"],
                                'harga_order_terkecil': item["harga_order_terkecil"],
                                'qty_besar': item["qty_besar"],
                                'harga_beli_terbesar': item["harga_beli_terbesar"],
                                'satuan_beli_terbesar': item["satuan_beli_terbesar"],
                                'tgl_ed': item["tgl_ed"],
                                'bonus': item["bonus"],
                                'gross': item["gross"],
                                'netto': item["netto"],
                                'kode_divisi_produk_id': kode_divisi.id if kode_divisi else False,
                                # 'kode_principal': item.get('kode_principal'),
                                'partner_id': partner_id,
                                'status_terkirim': item["status_terkirim"],
                                'status_barang': item["status_barang"],
                                'flagdepo': item["flagdepo"],
                                'kurir': item["kurir"],
                                'status_quo_barang': item["status_quo_barang"],
                                'catatan': item["catatan"],
                                'dosub': item["dosub"],
                                'bulando': item["bulando"],
                                'cbgitem': item["cbgitem"],
                                'tanggal_penarikan_awal': item["startdate"] if item["startdate"] not in ['0000-00-00', ''] else None,
                                'tanggal_penarikan_akhir': item["enddate"] if item["enddate"] not in ['0000-00-00', ''] else None,
                                'fetch_date': item["fetch_date"] if item["fetch_date"] not in ['0000-00-00', ''] else None,
                            })
                            records_created += 1
                            barang_datang_model.env.cr.commit()
                            _logger.info(f"Total Barang Datang {records_created} data created of total {total_records} data in Cabang {branch_name}.")

                return request.redirect(f'/web#action={action_id}&menu_id={menu_id}')

            except requests.exceptions.RequestException as e:
                if attempt < max_attempts:
                    _logger.info(f"Attempt {attempt} failed. Retrying in {attempt_delay} seconds.")
                    time.sleep(attempt_delay)
                else:
                    return json.dumps({'error': str(e)})