from odoo import http
from odoo.http import request, content_disposition
import mysql.connector
import logging
import json
import requests
import io
import xlsxwriter
import time
from datetime import datetime
from pytz import timezone
from requests.exceptions import ConnectionError, RequestException
from .constants import CABANG as list_cabang
from bigjson import FileReader
_logger = logging.getLogger(__name__)

class DataReplacingController(http.Controller):

    @http.route('/call_stored_procedure', type='http', auth='public', csrf=False)
    def data_replacing(self, **kwargs):
        connection_bisblg = None
        connection_master_pivot = None

        try:
            DataReplacing = http.request.env['data.replacing']
            record = DataReplacing.search([('vNamaCabang_id', '!=', False)], limit=1)
            if not record:
                return json.dumps({"status": "error", "message": "No record with non-empty vNamaCabang_id found"})
            records = record[0]
            _logger.info(f"Selected vNamaCabang_id: {records.vNamaCabang_id.display_name}")
            # record = DataReplacing.search([], limit=1)
            # if not record:
            #     return json.dumps({"status": "error", "message": "No record found"})
            
            CrudServerEnv = http.request.env['crud.server.env']
        

            # master_server_model = request.env['crud.server.env'].sudo()
            # master_server_id = master_server_model.search([('cabang')])

            server_env_record = CrudServerEnv.search([('cabang_master_id', '=', record.vNamaCabang_id.id)], limit=1) 
            _logger.info(f"server {server_env_record}")
            if not server_env_record:
                _logger.error(f"Server environment details not found for cabang_master_id: {record.vNamaCabang_id}")
                return json.dumps({"status": "error", "message": f"Server environment details not found for cabang_master_id: {record.vNamaCabang_id}"})

            _logger.info(f"Nama cabang dari replacing : {record.vNamaCabang_id.display_name}")
            _logger.info(f"Nama cabang dari Server list : {server_env_record.cabang_master_id.display_name}")
            _logger.info(f"IP : {server_env_record.ip}")
            _logger.info(f"port : {server_env_record.port}")
            _logger.info(f"username : {server_env_record.username}")
            _logger.info(f"password : {server_env_record.password}")
            _logger.info(f"Database : {server_env_record.database_name}")
            # Connection to bisblg database
            connection_bisblg = mysql.connector.connect(
                host=server_env_record.ip, port=server_env_record.port, user=server_env_record.username,
                password=server_env_record.password, database=server_env_record.database_name
            )
            # Connection to master_pivot database
            # connection_master_pivot = mysql.connector.connect(
            #     host=server_env_record.ip, port=server_env_record.port, user=server_env_record.username,
            #     password=server_env_record.password, database=server_env_record.database_name
            # )

            with connection_bisblg.cursor() as cursor:
                # Preparing parameters for the stored procedure
                    schoosedivorbrg_ids_str = ','.join(["'{}'".format(c.kode_divisi_produk) for c in record.schoosedivorbrg_ids])
                    call_statement = """
                        CALL pv_sp_replacing_cabang_corporate(
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        
                    """
                    parameters = [
                        record.vcabang, record.vNamaCabang_id.display_name,
                        record.vawal.strftime('%Y-%m-%d'), record.vakhir.strftime('%Y-%m-%d'),
                        record.speriodeawal, record.speriodeakhir,
                        schoosedivorbrg_ids_str, 'Divisi' if record.sdivproduk == 'Divisi' else 'Item',
                        record.sbonus, record.sTabSufffix
                    ]
                    
                    _logger.info(f"Executing stored procedure with params: {parameters}")
                    cursor.execute(call_statement, parameters)
                    connection_bisblg.commit()
        except mysql.connector.Error as err:
            _logger.error(f"Database error: {err}")
            return json.dumps({"status": "error", "message": str(err)})

        finally:
            # Close the connections if they're open
            if connection_bisblg and connection_bisblg.is_connected():
                connection_bisblg.close()
            if connection_master_pivot and connection_master_pivot.is_connected():
                connection_master_pivot.close()

        # return json.dumps({"status": "success", "message": "Operation completed successfully"})
        # menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Prinsipal Pajak')], limit=1)
        # menu_id = menu.id if menu else None
        # return request.redirect(f'/web#action=portal_report_bsp.action_redirect_to_import_data_replacing')
        return request.redirect(f'/data/replacing/external')

    @http.route('/data/replacing/external', auth='public', method=['GET'])
    def data_external(self, **kw):
        try:
            DataReplacing = http.request.env['data.replacing']
            record = DataReplacing.search([('vNamaCabang_id', '!=', False)], limit=1)
            if not record:
                return json.dumps({"status": "error", "message": "No record with non-empty vNamaCabang_id found"})
            records = record[0]

            # Get kode_cabang from res.company
            cabang_master_record = http.request.env['res.company'].search([('id', '=', records.vNamaCabang_id.id)], limit=1)
            if not cabang_master_record:
                return json.dumps({"status": "error", "message": "res.company record not found"})
            
            kode_cabang = cabang_master_record.kode_cabang.lower()  # Ensure kode_cabang is in lowercase

            # Construct the new URL with kode_cabang
            url1 = f"http://192.168.16.130/portal/bis_{kode_cabang}/Bisreport/getReplacingBarang"
            _logger.info(f"ini url external : {url1}")
            response1 = requests.get(url1)
            response1.raise_for_status()

            # Cek respons URL pertama
            if response1.status_code != 200:
                return json.dumps({"error": "First URL did not respond with status 200"})
            return request.redirect(f'/get_json_responses')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/data/replacing/external')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
                    
    @http.route('/get_json_responses', auth='public', method=['GET'])
    def get_json_responses(self, **kw):
        max_attempts = 3  # Maximum number of retry attempts
        attempt_delay = 5  # Delay between retry attempts in seconds
        menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Replacing')], limit=1)
        menu_id = menu.id if menu else None
        jakarta_tz = timezone('Asia/Jakarta')
        current_time = datetime.now(jakarta_tz)
        current_date_str = current_time.strftime('%Y-%m-%d')
        request.env.cr.execute(f"DELETE FROM data_replacing WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
        request.env.cr.commit()
        for attempt in range(1, max_attempts + 1):
            try:
                url2 = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getReplacingBarang/?kode_cabang={}"
                
                
                for branch_name, abbreviation in list_cabang.items():
                    current_int_url = url2.format(abbreviation.upper())
                    _logger.info(f"Currently importing Daily Stock data of Cabang {branch_name} to Portal BSP ERP")
                    
                    print(f"Memproses URL: {current_int_url}")
                    
                    # current_processed_branch = abbreviation
                    
                    _logger.info("Memproses URL: %s", current_int_url)
                    response2 = requests.get(current_int_url)
                    response2.raise_for_status()
                    # BigJSON sections
                    file_like_object = io.BytesIO(response2.content)
                    reader = FileReader(file_like_object)
                    data = reader.read()
                    data_array = data["data"]

                    data_replacing_model = request.env['data.replacing'].sudo()
                    total_records = len(data_array)
                    _logger.info(f"Received {total_records} data items for {branch_name} (URL: {current_int_url})")

                    records_created = 0
                    # Process each item in the chunk
                    for item in data_array:
                        fetch_date = item['fetch_date']
                        if fetch_date in ['0000-00-00', '']:
                            fetch_date = None  
                        existing_replacing = data_replacing_model.search([
                            ('kode_cabang', '=', item['kode_cabang']),
                            ('rb_index', '=', item['rb_index']),
                            ('fetch_date', '=', fetch_date)
                        ], limit=1)
                        if not existing_replacing:
                            data_replacing_model.create({
                                'kode_cabang': item['kode_cabang'],
                                'nama_cabang_id': item['nama_cabang'],
                                'kode_barang_id': item['kode_barang'],
                                'nama_barang': item['nama_barang'],
                                'kode_divisi_produk_id': item['kode_divisi_produk'],
                                'kode_principal': item['kode_principal'],
                                'kode_barang_principal': item['kode_barang_principal'],
                                'ssl_cbg_levelasal': item['ssl_cbg_levelasal'],
                                'ssl_cbg_levelkecil': item['ssl_cbg_levelkecil'],
                                'harga_beli_terkecil': item['harga_beli_terkecil'],
                                'stock_avail': item['stock_avail'],
                                'stock_avail_rp': item['stock_avail_rp'],
                                'pending': item['pending'],
                                'pending_rp': item['pending_rp'],
                                'intransit': item['intransit'],
                                'intransit_rp': item['intransit_rp'],
                                'orderr': item['orderr'],
                                'order_rp': item['order_rp'],
                                'ratio': item['ratio'],
                                'sales': item['sales'],
                                'sales_rp': item['sales_rp'],
                                'faktor_pengali': item['faktor_pengali'],
                                'ssl_fix': item['ssl_fix'],
                                'ket_divisi': item['ket_divisi'],
                                'flag_ratio': item['flag_ratio'],
                                'tgl_berlaku_ssl': item['tgl_berlaku_ssl'] if item['tgl_berlaku_ssl'] not in ['0000-00-00', ''] else None,
                                'stock_good': item['stock_good'],
                                'fetch_date': item['fetch_date'] if item['fetch_date'] not in ['0000-00-00', ''] else None,
                                'startdate': item['startdate'] if item['startdate'] not in ['0000-00-00', ''] else None,
                                'enddate': item['enddate'] if item['enddate'] not in ['0000-00-00', ''] else None,
                                'rb_index': item['rb_index'],
                                })
                            records_created += 1
                            _logger.info(f"Data Replacing Record created, data items for {branch_name}: {records_created}/{total_records}")
                            data_replacing_model.env.cr.commit()
                    data_to_delete = request.env['data.replacing'].sudo().search([('delete_after_process', '=', True)])
                    data_to_delete.unlink()
                    # if records_created:
                    #     remaining_data = data_array[records_created:]
                    #     request.session['remaining_data'] = remaining_data
                    #         # request.session['action_id'] = action_id
                    #     request.session['menu_id'] = menu_id
                    #     request.session['attempt'] = attempt
                    #     request.session['max_attempts'] = max_attempts
                    #     request.session['records_created'] = records_created
                    #     request.session['total_records'] = total_records
                    #     request.session['attempt_delay'] = attempt_delay

                    #     return request.redirect('/get_json_responses')
                    
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_attempts:
                    _logger.info(f"Attempt {attempt} failed. Retrying in {attempt_delay} seconds.")
                    time.sleep(attempt_delay)
                else:
                    return json.dumps({'error': str(e)})
        return request.redirect(f'/web#action=portal_report_bsp.action_portal_data_replacing&menu_id={menu_id}')    