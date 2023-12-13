from odoo import http
from odoo.http import request
import mysql.connector
import logging
import json
import requests
from datetime import datetime
from pytz import timezone
from requests.exceptions import ConnectionError, RequestException
from bigjson import FileReader
import io

_logger = logging.getLogger(__name__)

class MrpController(http.Controller):

    @http.route('/mrp/bpb', auth='public', method=['GET'])
    def get_mrp_bpb(self, **kw):
        try:
            # URL pertama
            url1 = "http://192.168.16.130/portal/mrp/Mrpreport/getBpb"
            response1 = requests.get(url1)
            response1.raise_for_status()

            # Cek respons URL pertama
            if response1.status_code != 200:
                _logger.error(f"First URL did not respond with status 200, status code: {response1.status_code}")
                return json.dumps({"error": "First URL did not respond with status 200"})
            else:
                _logger.info(f"First URL responded successfully with status 200. Response: {response1.json()}")

            # URL kedua
            url2 = "http://192.168.20.99/getmrBpb"
            response2 = requests.get(url2)
            response2.raise_for_status()

            # BigJSON sections
            file_like_object = io.BytesIO(response2.content)
            reader = FileReader(file_like_object)
            data = reader.read()
            data_array = data["data"]

            # Date adjustment section
            jakarta_tz = timezone('Asia/Jakarta')
            current_time = datetime.now(jakarta_tz)
            current_date_str = current_time.strftime('%Y-%m-%d')

            # Truncate sections
            request.env.cr.execute(f"DELETE FROM mrp_bpb WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
            request.env.cr.commit()
            mrp_bpb_model = request.env['mrp.bpb'].sudo()

            # data = response2.json()
            # Process the response from BigJSON
            for item in data_array:
                # existing_bpb = mrp_bpb_model.search([('ISS_NO', '=', item.get('ISS_NO'))], limit=1)
                fetch_date = item["fetch_date"]
                if fetch_date in ['0000-00-00', '']:
                    fetch_date = None  
                existing_bpb = mrp_bpb_model.search([
                    ('bpb_index', '=', item["bpb_index"]),
                    ('fetch_date', '=', fetch_date)
                ], limit=1)
                if not existing_bpb:
                    mrp_bpb_model.create({
                        'ISS_NO': item["ISS_NO"],
                        'ISS_DATE': item["ISS_DATE"],
                        'ISS_STATUS': item["ISS_STATUS"],
                        'DO_NO': item["DO_NO"],
                        'MO_NO': item["MO_NO"],
                        'MO_TYPE': item["MO_TYPE"],
                        'po_no': item["po_no"],
                        'PRODUCT_CODE': item["PRODUCT_CODE"],
                        'PRODUCT_DESC': item["PRODUCT_DESC"],
                        'prod_unit': item["prod_unit"],
                        'prod_group': item["prod_group"],
                        'LOT_NUMBER': item["LOT_NUMBER"],
                        'iss_qty': item["iss_qty"],
                        'expired_date': item["expired_date"] if item["expired_date"] not in ['0000-00-00', ''] else None,
                        'LOCATION_NO': item["LOCATION_NO"],
                        'CUSTOMER_CODE': item["CUSTOMER_CODE"],
                        'CUST_NAME': item["CUST_NAME"],
                        'exp_date': item["exp_date"] if item["exp_date"] not in ['0000-00-00', ''] else None,
                        'actual_date': item["actual_date"] if item["actual_date"] not in ['0000-00-00', ''] else None,
                        'loading_date': item["loading_date"] if item["loading_date"] not in ['0000-00-00', ''] else None,
                        'execdate': item["execdate"],
                        'exp_no': item["exp_no"],
                        'exp_status': item["exp_status"],
                        'forwarder': item["forwarder"],
                        'resi_number': item["resi_number"],
                        'jumlah': item["jumlah"],
                        'total_vol': item["total_vol"],
                        'total_weight': item["total_weight"],
                        'bpb_index': item["bpb_index"],
                        'fetch_date': item["fetch_date"] if item["fetch_date"] not in ['0000-00-00', ''] else None,

                    })
                    mrp_bpb_model.env.cr.commit()
            # data_to_delete = request.env['mrp.bpb'].sudo().search([('delete_after_process', '=', True)])
            # data_to_delete.unlink()

            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'BPB')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=portal_report_bsp.action_portal_mrp_bpb&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/mrp/bpb')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
            
    
    @http.route('/mrp/sla', auth='public', method=['GET'])
    def get_mrp_sla(self, **kw):
        try:
            # URL pertama
            url1 = "http://192.168.16.130/portal/mrp/Mrpreport/getSla/"
            response1 = requests.get(url1)
            response1.raise_for_status()

            # Cek respons URL pertama
            if response1.status_code != 200:
                _logger.error(f"First URL did not respond with status 200, status code: {response1.status_code}")
                return json.dumps({"error": "First URL did not respond with status 200"})
            else:
                _logger.info(f"First URL responded successfully with status 200. Response: {response1.json()}")

            # URL kedua
            url2 = "http://192.168.20.99/getSla"
            response2 = requests.get(url2)
            response2.raise_for_status()

            # BigJSON sections
            file_like_object = io.BytesIO(response2.content)
            reader = FileReader(file_like_object)
            data = reader.read()
            data_array = data["data"]

            # Date adjustment section
            jakarta_tz = timezone('Asia/Jakarta')
            current_time = datetime.now(jakarta_tz)
            current_date_str = current_time.strftime('%Y-%m-%d')

            # Truncate sections
            request.env.cr.execute(f"DELETE FROM mrp_sla WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
            request.env.cr.commit()
            mrp_sla_model = request.env['mrp.sla'].sudo()

            # data = response2.json()
            # Process the response from BigJSON
            for item in data_array:
                # existing_sla = mrp_sla_model.search([('ProductCode', '=', item.get('ProductCode'))])
                fetch_date = item["fetch_date"]
                if fetch_date in ['0000-00-00', '']:
                    fetch_date = None  
                existing_sla = mrp_sla_model.search([
                    ('sla_index', '=', item["sla_index"]),
                    ('fetch_date', '=', fetch_date)
                ], limit=1)
                if not existing_sla:
                    mrp_sla_model.create({
                        'productOwner': item["productOwner"],
                        'ProductionUnit': item["ProductionUnit"],
                        'ProductCode': item["ProductCode"],
                        'ProductName': item["ProductName"],
                        'UOMCodeDefault': item["UOMCodeDefault"],
                        'ProductCategory': item["ProductCategory"],
                        'MonthlyForecastQuantity': item["MonthlyForecastQuantity"],
                        'MORequest': item["MORequest"],
                        'MODelivery': item["MODelivery"],
                        'MOPendingQuantity': item["MOPendingQuantity"],
                        'WIPBalanceQty': item["WIPBalanceQty"],
                        'QuarantinedBalanceQuantity': item["QuarantinedBalanceQuantity"],
                        'QuarantinedHoldBalanceQuantity': item["QuarantinedHoldBalanceQuantity"],
                        'QuarantinedLastLotNo': item["QuarantinedLastLotNo"],
                        'ReleasedBalanceQuantity': item["ReleasedBalanceQuantity"],
                        'ReleasedBalanceHoldQuantity': item["ReleasedBalanceHoldQuantity"],
                        'ReleasedBalanceAndHoldQuantity': item["ReleasedBalanceAndHoldQuantity"],
                        'ReleasedLastLotNo': item["ReleasedLastLotNo"],
                        'TotalStockQuantity': item["TotalStockQuantity"],
                        'LevelTotalValuemonths': item["LevelTotalValuemonths"],
                        'ReadyStockQuantity': item["ReadyStockQuantity"],
                        'LevelReadyValuemonths': item["LevelReadyValuemonths"],
                        'PlantGroup': item["PlantGroup"],
                        'exeuid': item["exeuid"],
                        'exetime': item["exetime"] if item["exetime"] not in ['0000-00-00 00:00:00', ''] else None,
                        'sla_index': item["sla_index"],
                        'fetch_date': item["fetch_date"] if item["fetch_date"] not in ['0000-00-00', ''] else None,
                    })
                    mrp_sla_model.env.cr.commit()
            # data_to_delete = request.env['mrp.sla'].sudo().search([('delete_after_process', '=', True)])
            # data_to_delete.unlink()
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'SLA')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=portal_report_bsp.action_portal_mrp_sla&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/mrp/sla')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
            

    @http.route('/mrp/mo', auth='public', method=['GET'])
    def get_mrp_mo(self, **kw):
        try:
            # URL pertama
            url1 = "http://192.168.16.130/portal/mrp/Mrpreport/getMoPending/"
            response1 = requests.get(url1)
            response1.raise_for_status()

            # Cek respons URL pertama
            if response1.status_code != 200:
                _logger.error(f"First URL did not respond with status 200, status code: {response1.status_code}")
                return json.dumps({"error": "First URL did not respond with status 200"})
            else:
                _logger.info(f"First URL responded successfully with status 200. Response: {response1.json()}")

            # URL kedua
            url2 = "http://192.168.20.99/getMopending"
            response2 = requests.get(url2)
            response2.raise_for_status()

            # BigJSON sections
            file_like_object = io.BytesIO(response2.content)
            reader = FileReader(file_like_object)
            data = reader.read()
            data_array = data["data"]

            # Date adjustment section
            jakarta_tz = timezone('Asia/Jakarta')
            current_time = datetime.now(jakarta_tz)
            current_date_str = current_time.strftime('%Y-%m-%d')

            # Truncate sections
            request.env.cr.execute(f"DELETE FROM mrp_mo WHERE fetch_date > '{current_date_str}'::date - INTERVAL '1 day'")
            request.env.cr.commit()
            mrp_mo_model = request.env['mrp.mo'].sudo()

            # Process the response from BigJSON
            for item in data_array:
                # existing_mo = mrp_mo_model.search([('mo_no', '=', item["MoNo'))])
                fetch_date = item["fetch_date"]
                if fetch_date in ['0000-00-00', '']:
                    fetch_date = None  
                existing_mo = mrp_mo_model.search([
                    ('mop_index', '=', item["mop_index"]),
                    ('fetch_date', '=', fetch_date)
                ], limit=1)
                if not existing_mo:
                    mrp_mo_model.create({
                        'mo_no': item["MoNo"],
                        'mo_date': item["MoDate"] if item["MoDate"] not in ['0000-00-00 00:00:00', ''] else None,
                        'mo_type': item["MoType"],
                        'mo_group': item["MoGroup"],
                        'customer_code': item["CustomerCode"],
                        'customer': item["Customer"],
                        'order_status': item["OrderStatus"],
                        'product_code': item["ProductCode"],
                        'product_name': item["ProductDesc"],
                        'order_qty': item["OrderQty"],
                        'ship_qty': item["ShipQty"],
                        'pending_qty': item["PendingQty"],
                        'so_no': item["SoNo"],
                        'notes': item["note"],
                        'fetch_date': item["fetch_date"] if item["fetch_date"] not in ['0000-00-00', ''] else None,
                        'mop_index': item["mop_index"]
                    })
                    mrp_mo_model.env.cr.commit()


            data_to_delete = request.env['mrp.mo'].sudo().search([('delete_after_process', '=', True)])
            data_to_delete.unlink()
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'MO')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=portal_report_bsp.action_portal_mrp_mo&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/mrp/mo')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
            
            