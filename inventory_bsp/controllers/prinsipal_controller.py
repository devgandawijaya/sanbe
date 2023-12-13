from odoo import http
from odoo.http import request
import requests
from odoo.exceptions import UserError, AccessError
import logging
import json
from itertools import islice
from requests.exceptions import ConnectionError, RequestException

_logger = logging.getLogger(__name__)

class ImportProvinsiController(http.Controller):
    @http.route('/import/cabang', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_cabang(self, **kwargs):
        cabang_model = request.env['res.company'].sudo()
        _logger.info("Import cabang template function called")

        try:
            url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getCabang"
            response = requests.get(url)
            if response.status_code != 200:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()
            for item in data.get('data', []):
                existing_cabang = cabang_model.search([('name', '=', item.get('nama_cabang'))])
                kode_provinsi = request.env['res.country.state'].search([
                        ('name', '=', item.get('kode_provinsi'))
                    ], limit=1)
                mata_uang = request.env['res.currency'].search([
                        ('name', '=', item.get('kode_negara'))
                    ], limit=1)
                if not mata_uang:
                    mata_uang = request.env['res.currency'].search([
                        ('name', '=', 'IDR')
                    ], limit=1)
                karyawan = request.env['hr.employee'].search([
                    ('name', '=', item.get('id_karyawan'))
                    ], limit=1)
                if not existing_cabang:
                    cabang_model.create({
                            'kode_cabang': item.get('kode_cabang'),
                            'name': item.get('nama_cabang'),
                            'phone': item.get('tlp_cabang'),
                            'fax_cabang': item.get('fax_cabang'),
                            'email': item.get('email_cabang'),
                            'street': item.get('alamat_cabang'),
                            'vat': item.get('npwp_cabang'),
                            'tax_lock_date': item.get('npwp_tanggal') if item.get('npwp_tanggal') != '0000-00-00 00:00:00' else False,
                            'sk_mentri': item.get('sk_mentri'),
                            'nomor_seri_pajak': item.get('nomor_seri_pajak'),
                            'no_izin': item.get('no_izin'),
                            'akhir_bulan_berlaku': item.get('akhir_bulan_berlaku') if item.get('akhir_bulan_berlaku') != '0000-00-00 00:00:00' else False,
                            'penangung_jawab': item.get('penangung_jawab'),
                            'sik_aa': item.get('sik_aa'),
                            'tanggal_berdiri': item.get('tanggal_berdiri') if item.get('tanggal_berdiri') != '0000-00-00 00:00:00' else False,
                            'state_id': kode_provinsi.id if kode_provinsi else False,
                            'nik_kepala_cabang': item.get('nik_kepala_cabang'),
                            'no_izin_akses': item.get('no_izin_akses'),
                            'penanggung_jawab_alkes': item.get('penanggung_jawab_alkes'),
                            'sik_aa_alkes': item.get('sik_aa_alkes'),
                            'kagud': item.get('kagud'),
                            'karyawan_id': karyawan.id if karyawan else False,
                            'currency_id': mata_uang.id if mata_uang else False,
                            })
                else:
                    values_to_update = {
                        'kode_cabang': item.get('kode_cabang'),
                        'name': item.get('nama_cabang'),
                        'phone': item.get('tlp_cabang'),
                        'fax_cabang': item.get('fax_cabang'),
                        'email': item.get('email_cabang'),
                        'street': item.get('alamat_cabang'),
                        'vat': item.get('npwp_cabang'),
                        'tax_lock_date': item.get('npwp_tanggal') if item.get('npwp_tanggal') != '0000-00-00 00:00:00' else False,
                        'sk_mentri': item.get('sk_mentri'),
                        'nomor_seri_pajak': item.get('nomor_seri_pajak'),
                        'no_izin': item.get('no_izin'),
                        'akhir_bulan_berlaku': item.get('akhir_bulan_berlaku') if item.get('akhir_bulan_berlaku') != '0000-00-00 00:00:00' else False,
                        'penangung_jawab': item.get('penangung_jawab'),
                        'sik_aa': item.get('sik_aa'),
                        'tanggal_berdiri': item.get('tanggal_berdiri') if item.get('tanggal_berdiri') != '0000-00-00 00:00:00' else False,
                        'state_id': kode_provinsi.id if kode_provinsi else False,
                        'nik_kepala_cabang': item.get('nik_kepala_cabang'),
                        'no_izin_akses': item.get('no_izin_akses'),
                        'penanggung_jawab_alkes': item.get('penanggung_jawab_alkes'),
                        'sik_aa_alkes': item.get('sik_aa_alkes'),
                        'kagud': item.get('kagud'),
                        'karyawan_id': karyawan.id if karyawan else False,
                        'currency_id': mata_uang.id if mata_uang else False,
                    }
                    existing_cabang.write(values_to_update)
                cabang_model.env.cr.commit()

            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Cabang')], limit=1)
            menu_id = menu.id if menu else None
            return request.redirect(f'/web#action=inventory_bsp.action_res_company_menu&menu_id={menu_id}')

        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/cabang')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})