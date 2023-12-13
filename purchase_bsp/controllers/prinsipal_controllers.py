from odoo import http
from odoo.http import request
import requests
from odoo.exceptions import UserError, AccessError
import logging
import json
from itertools import islice
from requests.exceptions import ConnectionError, RequestException
from odoo.http import request
import requests

_logger = logging.getLogger(__name__)

class PrinsipalControllers(http.Controller):
    @http.route('/import-prinsipal-partner', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_prinsipal_partner(self, **kwargs):
        partner_model = request.env['res.partner'].sudo()
        currency_model = request.env['res.currency'].sudo()
        user_model = request.env['res.users'].sudo()
        _logger.info("Import Prinsipal Partner route is called.")

        try:
            url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/index"
            response = requests.get(url)
            if response.status_code != 200:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()
            res_data = data.get('data', [])

            for item in res_data:

                # Get currency_id
                existing_currency = currency_model.search([('active','=',False), ('name','=',item.get('mata_uang'))])
                if existing_currency.active == False:
                    existing_currency.write({'active':True})
                    existing_currency.env.cr.commit()

                # Get user_id
                existing_user = user_model.search([('login', '=', item.get('id_karyawan') + '@bsp.id')], limit=1)
                if not existing_user:
                    existing_user_id = user_model.create({
                        'name': item.get('id_karyawan').title(),
                        'login': item.get('id_karyawan') + '@bsp.id',
                        'password': item.get('id_karyawan') + '2023'
                    })
                    existing_user_id.env.cr.commit()
                else:
                    existing_user_id = existing_user.id
                
                existing_prinsipal = partner_model.search([('kode_principal', '=', item.get('kode_principal'))], limit=1)
                if not existing_prinsipal:
                    partner_id = partner_model.create({
                        'kode_principal': item.get('kode_principal'),
                        'name': item.get('nama_principal'),
                        'cp_logistik': item.get('cp_logistik').title(),
                        'cp_finance': item.get('cp_finance').title(),
                        'cp_marketing': item.get('cp_marketing').title(),
                        'phone': item.get('tlp_principal'),
                        'fax_principal': item.get('fax_principal'),
                        'street': item.get('alamat_principal'),
                        'email': item.get('email_principal'),
                        'vat': item.get('npwp_principal'),
                        'tanggal_bergabung': item.get('tanggal_bergabung') if item.get('tanggal_bergabung') != '0000-00-00' else False,
                        'tanggal_berhenti': item.get('tanggal_berhenti') if item.get('tanggal_berhenti') != '0000-00-00' else False,
                        'jenis_pengembalian': item.get('jenis_pengembalian'),
                        'percent_pembulat': item.get('percent_pembulatan'),
                        'diskon_faktur': item.get('disonfaktur'),
                        'faktur_ekslusif': item.get('faktur_eklusif'),
                        'ekslusif_awal': item.get('eklusif_awal') if item.get('eklusif_awal') != '0000-00-00' else False,
                        'ekslusif_akhir': item.get('eklusif_akhir') if item.get('eklusif_akhir') != '0000-00-00' else False,
                        'nama_bm': item.get('nama_bm'),
                        'date': item.get('time_stamp') if item.get('time_stamp') != '0000-00-00' else False,
                        'harga_acuan': item.get('harga_acuan'),
                        'nomor_nppkp': item.get('nomor_nppkp'),
                        'tgl_pkp': item.get('tgl_pkp') if item.get('tgl_pkp') != '0000-00-00' else False,
                        'currency_id': existing_currency.id,
                        'is_company': True,
                        'is_bsp_prinsipal': True
                    })
                    partner_id.write({'user_id':existing_user_id})
                    partner_id.env.cr.commit()

            action = request.env['ir.actions.act_window'].sudo().search([('name', '=', 'Vendors')], limit=1)
            action_id = action.id if action else None

            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Vendors')], limit=1)
            menu_id = menu.id if menu else None

            return request.redirect(f'/web#action={action_id}&menu_id={menu_id}')
        
        except requests.exceptions.RequestException as e:
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                return request.redirect(f'/import-prinsipal-partner')
            else:
                return json.dumps({'error': str(e)})

    # prinsipal Channel
    @http.route('/import/prinsipal/channel', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_prinsipal_channel(self, **kwargs):
        prinsipal_channel_model = request.env['prinsipal.channel'].sudo()
        _logger.info("Import prinsipal template function called")

        try:
            url = "http://192.168.16.130/microservice_internal/produk/prinsipal/getPrinsipalChanel"
            response = requests.get(url)
            if response.status_code != 200:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()
            count = 0
            for item in data.get('data', []):
                if count >= 50:
                    break
                existing_prinsipal_channel = prinsipal_channel_model.search([('kode_principal_chanel', '=', item.get('kode_principal_chanel'))])
                if not existing_prinsipal_channel:
                    vendor = request.env['res.partner'].search([
                        ('name', '=', item.get('nama_principal'))
                    ], limit=1)
                    prinsipal_channel_model.with_context(skip_external_api=True).create({
                            'kode_principal_chanel': item.get('kode_principal_chanel'),
                            'kode_principal': item.get('kode_principal'),
                            'nama_chanel': item.get('nama_chanel'),
                            'time_stamp': item.get('time_stamp') if item.get('time_stamp') != '0000-00-00' else False,
                            'nama_principal_id': vendor.id if vendor else False,
                            })
                    prinsipal_channel_model.env.cr.commit()
                count += 1

            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Vendor Channel')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=inventory_bsp.action_prinsipal_channel&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/prinsipal/channel')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})


    # prinsipal pajak
    @http.route('/import/prinsipal/pajak', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_prinsipal_pajak(self, **kwargs):
        prinsipal_pajak_model = request.env['prinsipal.pajak'].sudo()
        _logger.info("Import prinsipal template function called")
        user_model = request.env['res.users'].sudo()
        try:
            url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getPrinsipalPajak"
            response = requests.get(url)
            if response.status_code != 200:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()
            for item in data.get('data', []):
                existing_provinsi = prinsipal_pajak_model.search([('kode_pajak_prinsipal', '=', item.get('kode_pajak_prinsipal'))])
                if not existing_provinsi:
                    vendor = request.env['res.partner'].search([
                        ('name', '=', item.get('nama_principal'))
                    ], limit=1)
                    karyawan = user_model.search([('login', '=', item.get('id_karyawan') + '@bsp.id')], limit=1)
                    if not karyawan:
                        karyawan_id = user_model.create({
                            'name': item.get('id_karyawan').title(),
                            'login': item.get('id_karyawan') + '@bsp.id',
                            'password': item.get('id_karyawan') + '2023'
                        })
                        karyawan_id.env.cr.commit()
                    else:
                        karyawan_id = karyawan.id
                    prinsipal_pajak_model.with_context(skip_external_api=True).create({
                            'kode_pajak_prinsipal': item.get('kode_pajak_prinsipal'),
                            'kode_principal': item.get('kode_principal'),
                            'tanggal_pengajuan': item.get('tanggal_pengajuan') if item.get('tanggal_pengajuan') != '0000-00-00' else False,
                            'status_pajak': item.get('status_pajak'),
                            'karyawan_id': karyawan.id if karyawan else False,
                            'time_stamp': item.get('time_stamp') if item.get('time_stamp') != '0000-00-00' else False,
                            'time_create': item.get('time_create') if item.get('time_create') != '0000-00-00' else False,
                            'nama_principal_id': vendor.id if vendor else False,
                            })
                    prinsipal_pajak_model.env.cr.commit()

            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Vendor Pajak')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=inventory_bsp.action_prinsipal_pajak&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/prinsipal/pajak')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
        
    # prinsipal rekening
    @http.route('/import/prinsipal/rekening', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_prinsipal_rekening(self, **kwargs):
        prinsipal_rekening_model = request.env['prinsipal.rekening'].sudo()
        _logger.info("Import prinsipal template function called")
        user_model = request.env['res.users'].sudo()
        try:
            url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getPrinsipalBank"
            response = requests.get(url)
            if response.status_code != 200:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()
            for item in data.get('data', []):
                existing_provinsi = prinsipal_rekening_model.search([('nama_principal_id', '=', item.get('nama_principal'))])
                if not existing_provinsi:
                    vendor = request.env['res.partner'].search([
                        ('name', '=', item.get('nama_principal'))
                    ], limit=1)
                    karyawan = user_model.search([('login', '=', item.get('id_karyawan') + '@bsp.id')], limit=1)
                    if not karyawan:
                        karyawan_id = user_model.create({
                            'name': item.get('id_karyawan').title(),
                            'login': item.get('id_karyawan') + '@bsp.id',
                            'password': item.get('id_karyawan') + '2023'
                        })
                        karyawan_id.env.cr.commit()
                    else:
                        karyawan_id = karyawan.id
                    prinsipal_rekening_model.create({
                            'kode_rekening_principal': item.get('kode_rekening_principal'),
                            'kode_bank': item.get('kode_bank'),
                            'kode_principal': item.get('kode_principal'),
                            'an_rekening_principal': item.get('an_rekening_principal'),
                            'nama_bank': item.get('nama_bank'),
                            'karyawan_id': karyawan.id if karyawan else False,
                            'time_stamp': item.get('time_stamp') if item.get('time_stamp') != '0000-00-00  00:00:00' else False,
                            'nomor_rekening': item.get('nomor_rekening'),
                            'nama_principal_id': vendor.id if vendor else False,
                            })
                    prinsipal_rekening_model.env.cr.commit()

            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Vendor Rekening')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=inventory_bsp.action_prinsipal_rekening&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/prinsipal/rekening')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})