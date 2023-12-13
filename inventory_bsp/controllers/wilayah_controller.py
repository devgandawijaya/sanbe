from odoo import http
from odoo.http import request
import requests
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class ImportProvinsiController(http.Controller):

    @http.route('/import/provinsi', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_provinsi(self, **kwargs):
        wilayah_provinsi_model = request.env['wilayah.provinsi'].sudo()
        _logger.info("Import Provinsi function called")

        try:
            # Fetch data from the external service
            url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getProvinsi/"
            response = requests.get(url)
            
            # Check if the response is successful
            if response.status_code != 200:
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()

            # Process each item in the received data
            for item in data.get('data', []):
                existing_provinsi = wilayah_provinsi_model.search([('kode_provinsi', '=', item.get('kode_provinsi'))])
                if not existing_provinsi:
                    wilayah_provinsi_model.create({
                        'kode_provinsi': item.get('kode_provinsi'),
                        'id_negara': item.get('id_negara'),
                        'nama_negara': item.get('nama_negara'),
                        'nama_provinsi': item.get('nama_provinsi'),
                    })
                    # Commit the transaction after each record creation
                    wilayah_provinsi_model.env.cr.commit()
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Provinsi')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_wilayah_provinsi&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
        except Exception as e:
            _logger.error("Error importing data: %s", str(e))
            return "Error: " + str(e)


    @http.route('/import/kota', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_kota(self, **kwargs):
        wilayah_kota_model = request.env['wilayah.kota'].sudo()
        _logger.info("Import kota function called")

        try:
            # Ambil semua provinsi
            all_provinsi = request.env['wilayah.provinsi'].search([])
            for provinsi in all_provinsi:
                url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getKabupatenKota/"
                headers = {'Content-Type': 'application/json'}
                body = json.dumps({"kode_provinsi": provinsi.kode_provinsi})

                # Lakukan permintaan POST
                response = requests.post(url, headers=headers, data=body)
                if response.status_code != 200:
                    _logger.error('Error fetching data for provinsi %s: Status code %s, Response: %s', provinsi.kode_provinsi, response.status_code, response.text)
                    continue  # Lanjut ke provinsi berikutnya jika terjadi error

                data = response.json()

                # Proses setiap item dalam data yang diterima
                for item in data.get('data', []):
                    existing_kota = wilayah_kota_model.search([('kode_kabkot', '=', item.get('kode_kabkot'))])
                    if not existing_kota:
                        wilayah_kota_model.create({
                            'kode_kabkot': item.get('kode_kabkot'),
                            'kode_provinsi_id': provinsi.id,
                            'nama_kabupaten_kota': item.get('nama_kabupaten_kota'),
                        })
                        # Commit transaksi setelah setiap penciptaan record
                        wilayah_kota_model.env.cr.commit()

            # Konstruksi URL pengalihan dengan ID menu yang ditemukan secara dinamis
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Kota')], limit=1)
            menu_id = menu.id if menu else None
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_wilayah_kota&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_wilayah_kota')
        except Exception as e:
            _logger.error("Error importing data: %s", str(e))
            return "Error: " + str(e)

    @http.route('/import/kecamatan', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_kecamatan(self, **kwargs):
        wilayah_kecamatan_model = request.env['wilayah.kecamatan'].sudo()
        _logger.info("Import kecamatan function called")

        try:
            # Ambil semua provinsi
            all_kota = request.env['wilayah.kota'].search([])
            for kota in all_kota:
                url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getKecamatan/"
                headers = {'Content-Type': 'application/json'}
                body = json.dumps({"kode_kabkot": kota.kode_kabkot})

                # Lakukan permintaan POST
                response = requests.post(url, headers=headers, data=body)
                if response.status_code != 200:
                    _logger.error('Error fetching data for kota %s: Status code %s, Response: %s', kota.kode_kabkot, response.status_code, response.text)
                    continue  # Lanjut ke provinsi berikutnya jika terjadi error

                data = response.json()

                # Proses setiap item dalam data yang diterima
                for item in data.get('data', []):
                    existing_kecamatan = wilayah_kecamatan_model.search([('id_kecamatan', '=', item.get('id_kecamatan'))])
                    if not existing_kecamatan:
                        wilayah_kecamatan_model.create({
                            'id_kecamatan': item.get('id_kecamatan'),
                            'kode_kabkot_id': kota.id,
                            'nama_kecamatan': item.get('nama_kecamatan'),
                        })
                        # Commit transaksi setelah setiap penciptaan record
                        wilayah_kecamatan_model.env.cr.commit()

            # Konstruksi URL pengalihan dengan ID menu yang ditemukan secara dinamis
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Kecamatan')], limit=1)
            menu_id = menu.id if menu else None
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_wilayah_kecamatan&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_wilayah_kecamatan')
        except Exception as e:
            _logger.error("Error importing data: %s", str(e))
            return "Error: " + str(e)


    @http.route('/import/kelurahan', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_kelurahan(self, **kwargs):
        wilayah_kelurahan_model = request.env['wilayah.kelurahan'].sudo()
        _logger.info("Import kelurahan function called")

        try:
            # Ambil semua provinsi
            all_kecamatan = request.env['wilayah.kecamatan'].search([])
            for kecamatan in all_kecamatan:
                url = "http://192.168.16.130/microservice_internal/produk/Prinsipal/getKelurahan/"
                headers = {'Content-Type': 'application/json'}
                body = json.dumps({"id_kecamatan": kecamatan.id_kecamatan})

                # Lakukan permintaan POST
                response = requests.post(url, headers=headers, data=body)
                if response.status_code != 200:
                    _logger.error('Error fetching data for kecamatan %s: Status code %s, Response: %s', kecamatan.id_kecamatan, response.status_code, response.text)
                    continue  # Lanjut ke provinsi berikutnya jika terjadi error

                data = response.json()

                # Proses setiap item dalam data yang diterima
                for item in data.get('data', []):
                    existing_kelurahan = wilayah_kelurahan_model.search([('id_kelurahan', '=', item.get('id_kelurahan'))])
                    if not existing_kelurahan:
                        wilayah_kelurahan_model.create({
                            'id_kelurahan': item.get('id_kelurahan'),
                            'id_kecamatan_id': kecamatan.id,
                            'nama_kelurahan': item.get('nama_kelurahan'),
                            'kode_pos': item.get('kode_pos'),
                        })
                        # Commit transaksi setelah setiap penciptaan record
                        wilayah_kelurahan_model.env.cr.commit()

            # Konstruksi URL pengalihan dengan ID menu yang ditemukan secara dinamis
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'kelurahan')], limit=1)
            menu_id = menu.id if menu else None
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_wilayah_kelurahan&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_wilayah_kelurahan')
        except Exception as e:
            _logger.error("Error importing data: %s", str(e))
            return "Error: " + str(e)
