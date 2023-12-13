from odoo import http
from odoo.http import request
import mysql.connector
import logging
import requests
import time
import json
from datetime import datetime
from pytz import timezone
from requests.exceptions import ConnectionError, RequestException
from .constants import CABANG as list_cabang
from bigjson import FileReader
import io

_logger = logging.getLogger(__name__)

class KonsolidasiController(http.Controller):
    @http.route('/import/konsolidasi', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_konsolidasi(self, **kwargs):
        wilayah_konsolidasi_model = request.env['konsolidasi.master'].sudo()
        _logger.info("Import konsolidasi function called")
        max_attempts = 3  # Maximum number of retry attempts
        attempt_delay = 5  # Delay between retry attempts in seconds
        menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Konsolidasi Master')], limit=1)
        menu_id = menu.id if menu else None
        jakarta_tz = timezone('Asia/Jakarta')
        current_time = datetime.now(jakarta_tz)
        current_date_str = current_time.strftime('%Y-%m-%d')
        request.env.cr.execute(f"DELETE FROM konsolidasi_master WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
        request.env.cr.commit()
        for attempt in range(1, max_attempts + 1):
            try:
                url = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getKonsolidasi/?kode_cabang={}"
                for branch_name, abbreviation in list_cabang.items():
                    current_int_url = url.format(abbreviation.upper())
                    _logger.info(f"Currently importing Daily Stock data of Cabang {branch_name} to Portal BSP ERP")
                    _logger.info("Memproses URL: %s", current_int_url)
                    response = requests.get(current_int_url)
                    
                    if response.status_code != 200:
                        return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)
                    # BigJSON sections
                    file_like_object = io.BytesIO(response.content)
                    reader = FileReader(file_like_object)
                    data = reader.read()
                    data_array = data["data"]
                    
                    total_records = len(data_array)
                    _logger.info(f"Received {total_records} data items for {branch_name} (URL: {current_int_url})")
                    records_created = 0
                    for item in data_array:
                        fetch_date = item['fetch_date']
                        if fetch_date in ['0000-00-00', '']:
                            fetch_date = None  
                        existing_konsolidasi = wilayah_konsolidasi_model.search([
                            ('kode_cabang_id', '=', item['kode_cabang']),
                            ('km_index', '=', item['km_index']),
                            ('fetch_date', '=', fetch_date)
                        ], limit=1)
                        if not existing_konsolidasi:
                            wilayah_konsolidasi_model.create({
                                'kode_cabang_id': item['kode_cabang'],
                                'kode_gudang_id': item['kode_gudang'],
                                'kode_barang_id': item['kode_barang'],
                                'satuan_purchaselvl': item['satuan_purchaselvl'],
                                'satuan_Yjual_kecil': item['satuan_Yjual_kecil'],
                                'satuan_sp_terkecil': item['satuan_sp_terkecil'],
                                'satuan_faktur_terkecil': item['satuan_faktur_terkecil'],
                                'satuan_sp': item['satuan_sp'],
                                'satuan_sales': item['satuan_sales'],
                                'flag_barang': item['flag_barang'],
                                'sp_kode_jenis_jual': item['sp_kode_jenis_jual'],
                                'sp_banded': item['sp_banded'],
                                'no_referensi_order': item['no_referensi_order'],
                                'ponumber': item['ponumber'],
                                'pomtc': item['pomtc'],
                                'kode_salesman': item['kode_salesman'],
                                'flagsp': item['flagsp'],
                                'flagsales': item['flagsales'],
                                'via': item['via'],
                                'status_sp': item['status_sp'],
                                'no_batch': item['no_batch'],
                                'kode_pelanggan': item['kode_pelanggan'],
                                'no_faktur': item['no_faktur'],
                                'jenis_transaksi': item['jenis_transaksi'],
                                'jenis_pembayaran': item['jenis_pembayaran'],
                                'kredit_lunak': item['kredit_lunak'],
                                'jenis_faktur': item['jenis_faktur'],
                                'no_reff_retur': item['no_reff_retur'],
                                'no_referensi': item['no_referensi'],
                                'id_program_diskon': item['id_program_diskon'],
                                'id_program_promosi': item['id_program_promosi'],
                                'id_program_voucher': item['id_program_voucher'],
                                'sales_depo': item['sales_depo'],
                                'ket_retur': item['ket_retur'],
                                'status_barang': item['status_barang'],
                                'kode_promosi_principal': item['kode_promosi_principal'],
                                'kode_rayon_kolektor': item['kode_rayon_kolektor'],
                                'no_delivery': item['no_delivery'],
                                'no_faktur_pajak': item['no_faktur_pajak'],
                                'kc_promosi': item['kc_promosi'],
                                'sp_total_harga': item['sp_total_harga'],
                                'sp_ppn': item['sp_ppn'],
                                'sp_diskon': item['sp_diskon'],
                                'sp_potongan': item['sp_potongan'],
                                'unitprice': item['unitprice'],
                                'qtyorder': item['qtyorder'],
                                'qtyterpenuhi': item['qtyterpenuhi'],
                                'diskonsp1': item['diskonsp1'],
                                'diskonsp2': item['diskonsp2'],
                                'hargasat_terbesar': item['hargasat_terbesar'],
                                'hargasat_terkecil': item['hargasat_terkecil'],
                                'qty_faktur': item['qty_faktur'],
                                'hargasat_faktur': item['hargasat_faktur'],
                                'qty_purchase_level': item['qty_purchase_level'],
                                'hargasat_purchase_level': item['hargasat_purchase_level'],
                                'qty_YJual_terkecil': item['qty_YJual_terkecil'],
                                'hargasat_YJual_terkecil': item['hargasat_YJual_terkecil'],
                                'gross': item['gross'],
                                'diskon1': item['diskon1'],
                                'diskon2': item['diskon2'],
                                'cash_diskon': item['cash_diskon'],
                                'potongan': item['potongan'],
                                'netto': item['netto'],
                                'harga_mtc': item['harga_mtc'],
                                'harga_ttc': item['harga_ttc'],
                                'gross_pricelist': item['gross_pricelist'],
                                'harga_penyetaraan': item['harga_penyetaraan'],
                                'bsp_diskon_khusus': item['bsp_diskon_khusus'],
                                'principal_diskon_khusus': item['principal_diskon_khusus'],
                                'principal_cn': item['principal_cn'],
                                'bsp_cn': item['bsp_cn'],
                                'tonase': item['tonase'],
                                'kubikasi': item['kubikasi'],
                                'bsp_share': item['bsp_share'],
                                'principal_share': item['principal_share'],
                                'gross_faktur': item['gross_faktur'],
                                'total_faktur': item['total_faktur'],
                                'prc_prosen_diskon1': item['prc_prosen_diskon1'],
                                'prc_value_diskon1': item['prc_value_diskon1'],
                                'prc_prosen_diskon2': item['prc_prosen_diskon2'],
                                'prc_value_diskon2': item['prc_value_diskon2'],
                                'prc_prosen_diskon3': item['prc_prosen_diskon3'],
                                'prc_value_diskon3': item['prc_value_diskon3'],
                                'prc_prosen_diskon4': item['prc_prosen_diskon4'],
                                'prc_value_diskon4': item['prc_value_diskon4'],
                                'prc_prosen_diskon5': item['prc_prosen_diskon5'],
                                'prc_value_diskon5': item['prc_value_diskon5'],
                                'total_bayar': item['total_bayar'],
                                'diskon_headerfk': item['diskon_headerfk'],
                                'potongan_headerfk': item['potongan_headerfk'],
                                'hna': item['hna'],
                                'sub_total': item['sub_total'],
                                'diskon_item': item['diskon_item'],
                                'extra': item['extra'],
                                'cash_diskon_recalculate': item['cash_diskon_recalculate'],
                                'nom_ppn': item['nom_ppn'],
                                'ppn_td_std': item['ppn_td_std'],
                                'ppn_td_sdrhn': item['ppn_td_sdrhn'],
                                'bebas_ppn_std': item['bebas_ppn_std'],
                                'bebas_ppn_sdrhn': item['bebas_ppn_sdrhn'],
                                'jml_pajak': item['jml_pajak'],
                                'tgl_referensi_order': item['tgl_referensi_order'] if item['tgl_referensi_order'] not in ['0000-00-00', ''] else None,
                                'podate': item['podate'] if item['podate'] not in ['0000-00-00', ''] else None,
                                'tglpomanual': item['tglpomanual'] if item['tglpomanual'] not in ['0000-00-00', ''] else None,
                                'tgledsp': item['tgledsp'] if item['tgledsp'] not in ['0000-00-00', ''] else None,
                                'tgl_faktur': item['tgl_faktur'] if item['tgl_faktur'] not in ['0000-00-00', ''] else None,
                                'tgl_jatuh_tempo': item['tgl_jatuh_tempo'] if item['tgl_jatuh_tempo'] not in ['0000-00-00', ''] else None,
                                'tgl_permintaan_kirim': item['tgl_permintaan_kirim'] if item['tgl_permintaan_kirim'] not in ['0000-00-00', ''] else None,
                                'delivery_date': item['delivery_date'] if item['delivery_date'] not in ['0000-00-00', ''] else None,
                                'tgl_mulai_overdue': item['tgl_mulai_overdue'] if item['tgl_mulai_overdue'] not in ['0000-00-00', ''] else None,
                                'tgl_referensi': item['tgl_referensi'] if item['tgl_referensi'] not in ['0000-00-00', ''] else None,
                                'tgl_faktur_pajak': item['tgl_faktur_pajak'] if item['tgl_faktur_pajak'] not in ['0000-00-00', ''] else None,
                                'kadaluarsa': item['kadaluarsa'] if item['kadaluarsa'] not in ['0000-00-00', ''] else None,
                                'last_update': item['last_update'] if item['last_update'] not in ['0000-00-00 00:00:00', ''] else None,
                                'fetch_date': item['fetch_date'] if item['fetch_date'] not in ['0000-00-00', ''] else None,
                                'km_index': item['km_index'],
                                })
                            records_created += 1
                            _logger.info(f"Data Replacing Record created, data items for {branch_name}: {records_created}/{total_records}")
                            wilayah_konsolidasi_model.env.cr.commit()

            except requests.exceptions.RequestException as e:
                if attempt < max_attempts:
                    _logger.info(f"Attempt {attempt} failed. Retrying in {attempt_delay} seconds.")
                    time.sleep(attempt_delay)
                else:
                    return json.dumps({'error': str(e)})
        return request.redirect(f'/web#action=portal_report_bsp.action_portal_konsolidasi_master&menu_id={menu_id}')   