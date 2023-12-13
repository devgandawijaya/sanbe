from odoo import http, exceptions
from odoo.http import request
import requests
from requests import Session
from odoo.exceptions import UserError, AccessError
import logging
import json
import time
from requests.exceptions import ConnectionError, RequestException


_logger = logging.getLogger(__name__)

class ImportProvinsiController(http.Controller):
    @http.route('/import/product', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product(self, **kwargs):
        product_model = request.env['product.template'].sudo()
        _logger.info("Import Product template function called")

        try:
            url = "http://192.168.16.130/microservice_internal/produk/produk/"
            response = requests.get(url)

            if response.status_code != 200:
                _logger.error(f"Failed to fetch data. Status code: {response.status_code}")
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)
            data = response.json()

            for item in data.get('data', []):
                existing_provinsi = product_model.search([('kode_barang', '=', item.get('kode_barang'))])
                purchasing_level_value = item.get('purchasing_level')
                if purchasing_level_value not in ['YA', 'TIDAK']:
                    _logger.error("Invalid value for purchasing_level: %s", purchasing_level_value)
                    continue
                kelompok_barang = request.env['product.kelompok'].search([
                    ('nama_kelompok_barang', '=', item.get('nama_kelompok_barang'))
                    ], limit=1)
                kode_divisi = request.env['product.divisi'].search([
                    ('kode_divisi_produk', '=', item.get('kode_divisi_produk'))
                    ], limit=1)
                kode_barang_dinkes = request.env['product.barang.dinkes'].search([
                    ('kode_barang_dinkes', '=', item.get('kode_barang_dinkes'))
                    ], limit=1)
                nama_categories = request.env['product.category'].search([
                    ('name', '=', item.get('nama_kategori'))
                    ], limit=1)
                regis_obat = request.env['product.registrasi.obat'].search([
                    ('name', '=', item.get('kode_register_obat'))
                    ], limit=1)
                if not regis_obat:
                    regis_obat = request.env['product.registrasi.obat'].create({
                        'name': item.get('kode_register_obat'),
                        })
                karyawan_name = item.get('id_karyawan', '').strip()
                if karyawan_name:
                    karyawan = request.env['res.users'].search([('login', '=', karyawan_name)], limit=1)
                    if not karyawan:
                        try:
                            karyawan = request.env['res.users'].sudo().create({
                                'name': karyawan_name,
                                'login': karyawan_name,
                            })
                        except AccessError as e:
                            _logger.error(f"Access Error when creating user: {e}")
                            continue 
                else:
                    karyawan = None
                    
                if existing_provinsi:
                    existing_provinsi.with_context(skip_external_api_update=True).write({
                        'kode_barang': item.get('kode_barang'),
                        'kode_kelompok_barang': item.get('kode_kelompok_barang'),
                        'nama_kelompok_barang_id': kelompok_barang.id if kelompok_barang else False,
                        'kode_divisi_produk_id': kode_divisi.id if kode_divisi else False,
                        'nama_divisi_produk': item.get('nama_divisi_produk'),
                        'kode_barang_dinkes_id': kode_barang_dinkes.id if kode_barang_dinkes else False,
                        'kode_register_obat_id': regis_obat.id if regis_obat else False,
                        'kode_kategori_barang': item.get('kode_kategori_barang'),
                        'nama_kategori_id': nama_categories.id if nama_categories else False,
                        'nama_barang': item.get('nama_barang'),
                        'name': item.get('nama_barang'),  
                        'harga_jual': item.get('harga_jual'),
                        'list_price': item.get('harga_jual'),
                        'standard_price': item.get('harga_jual'),
                        'harga_beli': item.get('harga_beli'),
                        'harga_tac': item.get('harga_tac'),
                        'harga_spreading': item.get('harga_spreading'),
                        'tanggal_discontinue': item.get('tanggal_discontinue') if item.get('tanggal_discontinue') not in [None, '0000-00-00 00:00:00'] else False,
                        'std_lead_time': item.get('std_lead_time'),
                        'pengali': item.get('pengali'),
                        'tempo': item.get('tempo'),
                        'purchasing_level': purchasing_level_value,
                        'karyawan_id': karyawan.id if karyawan else False,
                        'time_stamp': item.get('time_stamp') if item.get('time_stamp') not in [None, '0000-00-00 00:00:00'] else False,
                    })
                else:
                    product_model.with_context(skip_external_api=True).create({
                        'kode_barang': item.get('kode_barang'),
                        'kode_kelompok_barang': item.get('kode_kelompok_barang'),
                        'nama_kelompok_barang_id': kelompok_barang.id if kelompok_barang else False,
                        'kode_divisi_produk_id': kode_divisi.id if kode_divisi else False,
                        'nama_divisi_produk': item.get('nama_divisi_produk'),
                        'kode_barang_dinkes_id': kode_barang_dinkes.id if kode_barang_dinkes else False,
                        'kode_register_obat_id': regis_obat.id if regis_obat else False,
                        'kode_kategori_barang': item.get('kode_kategori_barang'),
                        'nama_kategori_id': nama_categories.id if nama_categories else False,
                        'nama_barang': item.get('nama_barang'),
                        'name': item.get('nama_barang'),  
                        'harga_jual': item.get('harga_jual'),
                        'list_price': item.get('harga_jual'),
                        'standard_price': item.get('harga_jual'),
                        'harga_beli': item.get('harga_beli'),
                        'harga_tac': item.get('harga_tac'),
                        'harga_spreading': item.get('harga_spreading'),
                        'tanggal_discontinue': item.get('tanggal_discontinue') if item.get('tanggal_discontinue') not in [None, '0000-00-00 00:00:00'] else False,
                        'std_lead_time': item.get('std_lead_time'),
                        'pengali': item.get('pengali'),
                        'tempo': item.get('tempo'),
                        'purchasing_level': purchasing_level_value,
                        'karyawan_id': karyawan.id if karyawan else False,
                        'time_stamp': item.get('time_stamp') if item.get('time_stamp') not in [None, '0000-00-00 00:00:00'] else False,
                    })
                    # Commit the transaction after each record creation
                    _logger.info("Imported Product: %s, Kode Barang: %s", item.get('nama_barang'), item.get('kode_barang'))
                    product_model.env.cr.commit()
                    _logger.info(f"Data yang ter GET : {product_model}")
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Products')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=stock.product_template_action_product&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=stock.product_template_action_product')
        except requests.exceptions.RequestException as e:
            _logger.error(f"Request Exception: {e}")
            return request.redirect(f'/import/product')
            # return json.dumps({'error': str(e)})
        except Exception as e:
            _logger.error(f"Unexpected Exception: {e}")
            # return json.dumps({'error': 'Unexpected error occurred'})
            return request.redirect(f'/import/product')

    # product Category
    @http.route('/import/product/category', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product_category(self, **kwargs):
        product_category_model = request.env['product.category'].sudo()
        _logger.info("Import Provinsi function called")

        try:
            # Fetch data from the external service
            url = "http://192.168.16.130/microservice_internal/produk/produk/geKategoriProduk/"
            response = requests.get(url)
            
            # Check if the response is successful
            if response.status_code != 200:
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()

            # Process each item in the received data
            for item in data.get('data', []):
                existing_provinsi = product_category_model.search([('kode_kategori_barang', '=', item.get('kode_kategori_barang'))])
                if not existing_provinsi:
                    karyawan_name = item.get('id_karyawan', '').strip()
                    if karyawan_name:
                        karyawan = request.env['res.users'].search([('login', '=', karyawan_name)], limit=1)
                        if not karyawan:
                            try:
                                karyawan = request.env['res.users'].sudo().create({
                                    'name': karyawan_name,
                                    'login': karyawan_name,
                                    # Add other necessary fields like email, password, etc.
                                })
                            except AccessError as e:
                                _logger.error(f"Access Error when creating user: {e}")
                                continue  # Skip this iteration if user creation fails
                    else:
                        karyawan = None
                    product_category_model.create({
                        'kode_kategori_barang': item.get('kode_kategori_barang'),
                        'name': item.get('nama_kategori'),
                        'karyawan_id': karyawan.id if karyawan else False,
                        'time_stamp': item.get('time_stamp') if item.get('time_stamp') != '0000-00-00 00:00:00' else False
                    })
                    # Commit the transaction after each record creation
                    product_category_model.env.cr.commit()
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Product Category')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=product.product_category_action_form&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=product.product_category_action_form')
        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/product/category')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
        

    # product kelompok
    @http.route('/import/product/kelompok', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product_kelompok(self, **kwargs):
        product_kelompok_model = request.env['product.kelompok'].sudo()
        _logger.info("Import Provinsi function called")

        try:
            # Fetch data from the external service
            url = "http://192.168.16.130/microservice_internal/produk/produk/getKelompokProduk/"
            response = requests.get(url)
            
            # Check if the response is successful
            if response.status_code != 200:
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()

            # Process each item in the received data
            for item in data.get('data', []):
                existing_provinsi = product_kelompok_model.search([('kode_kelompok_barang', '=', item.get('kode_kelompok_barang'))])
                if not existing_provinsi:
                    karyawan_name = item.get('id_karyawan', '').strip()
                    if karyawan_name:
                        karyawan = request.env['res.users'].search([('login', '=', karyawan_name)], limit=1)
                        if not karyawan:
                            try:
                                karyawan = request.env['res.users'].sudo().create({
                                    'name': karyawan_name,
                                    'login': karyawan_name,
                                    # Add other necessary fields like email, password, etc.
                                })
                            except AccessError as e:
                                _logger.error(f"Access Error when creating user: {e}")
                                continue  # Skip this iteration if user creation fails
                    else:
                        karyawan = None
                    product_kelompok_model.create({
                        'kode_kelompok_barang': item.get('kode_kelompok_barang'),
                        'nama_kelompok_barang': item.get('nama_kelompok_barang'),
                        'na_kelompok_barang': item.get('na_kelompok_barang'),
                        'karyawan_id': karyawan.id if karyawan else False,
                        'time_stamp': item.get('time_stamp') if item.get('time_stamp') != '0000-00-00 00:00:00' else False
                    })
                    # Commit the transaction after each record creation
                    product_kelompok_model.env.cr.commit()
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Product Kelompok')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_product_kelompok&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_product_kelompok')
        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/product/kelompok')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
        
    # product divisi
    @http.route('/import/product/divisi', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product_divisi(self, **kwargs):
        product_divisi_model = request.env['product.divisi'].sudo()
        _logger.info("Import Provinsi function called")
        user_model = request.env['res.users'].sudo()
        try:
            # Fetch data from the external service
            url = "http://192.168.16.130/microservice_internal/produk/produk/getDivisiProduk"
            response = requests.get(url)
            # Check if the response is successful
            if response.status_code != 200:
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)
            data = response.json()
            # Process each item in the received data
            for item in data.get('data', []):
                existing_provinsi = product_divisi_model.search([('kode_divisi_produk', '=', item.get('kode_divisi_produk'))])
                id_karyawan = item.get('id_karyawan')
                if id_karyawan is None:
                    _logger.error(f"Missing 'id_karyawan' for item: {item}")
                    continue  # Skip this item or handle it as you see fit

                karyawan_login = f'{id_karyawan}@bsp.id'
                karyawan = user_model.search([('login', '=', karyawan_login)], limit=1)
                if not karyawan:
                    karyawan_id = user_model.create({
                        'name': id_karyawan.title(),
                        'login': karyawan_login,
                        'password': id_karyawan + '2023'
                    })
                    karyawan_id.env.cr.commit()
                else:
                    karyawan_id = karyawan.id
                        
                kode_prinsipal = item.get('kode_prinsipale')
                if kode_prinsipal:
                    partner = request.env['res.partner'].search([('kode_principal', '=', kode_prinsipal)], limit=1)
                    partner_id = partner.id if partner else False
                else:
                    partner_id = False
                if not existing_provinsi:
                    product_divisi_model.create({
                        'kode_divisi_produk': item.get('kode_divisi_produk'),
                        # 'kode_prinsipal': item.get('kode_prinsipale'),
                        'partner_id': partner_id,
                        'nama_divisi_produk': item.get('nama_divisi_produk'),
                        'na_divisi_produk': item.get('na_divisi_produk'),
                        'karyawan_id': karyawan.id if karyawan else False,
                        'exclusive': item.get('exclusive'),
                        'vaccine': item.get('vaccine'),
                        'time_stime': item.get('time_stime') if item.get('time_stime') != '0000-00-00 00:00:00' else False
                    })
                else:
                    existing_provinsi.write({
                        'kode_divisi_produk': item.get('kode_divisi_produk'),
                        # 'kode_prinsipal': item.get('kode_prinsipale'),
                        'partner_id': partner_id,
                        'nama_divisi_produk': item.get('nama_divisi_produk'),
                        'na_divisi_produk': item.get('na_divisi_produk'),
                        'karyawan_id': karyawan.id if karyawan else False,
                        'exclusive': item.get('exclusive'),
                        'vaccine': item.get('vaccine'),
                        'time_stime': item.get('time_stime') if item.get('time_stime') != '0000-00-00 00:00:00' else False
                    })
                    # Commit the transaction after each record creation
            product_divisi_model.env.cr.commit()
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Product Divisi')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_product_divisi&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_product_divisi')
        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/product/divisi')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
        
    # product ppn
    @http.route('/import/product/ppn', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product_ppn(self, **kwargs):
        product_ppn_model = request.env['product.ppn'].sudo()
        _logger.info("Import Provinsi function called")

        try:
            # Fetch data from the external service
            url = "http://192.168.16.130/microservice_internal/produk/produk/getPpnProduk/"
            response = requests.get(url)
            
            # Check if the response is successful
            if response.status_code != 200:
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()

            # Process each item in the received data
            for item in data.get('data', []):
                existing_provinsi = product_ppn_model.search([('kode_barang_ppn', '=', item.get('kode_barang_ppn'))])
                if not existing_provinsi:
                    kode_barang = request.env['product.template'].search([
                            ('kode_barang', '=', item.get('kode_barang'))
                        ], limit=1)
                    product_ppn_model.create({
                        'kode_barang_ppn': item.get('kode_barang_ppn'),
                        'kode_barang_id': kode_barang.id if kode_barang else False,
                        'tanggal_mulai_berlaku': item.get('tanggal_mulai_berlaku') if item.get('tanggal_mulai_berlaku') != '0000-00-00' else False,
                        'PPN': item.get('PPN'),
                        'bebas_ppn': item.get('bebas_ppn'),
                        'tanggal_berakhir_ppn': item.get('tanggal_berakhir_ppn') if item.get('tanggal_berakhir_ppn') != '0000-00-00' else False
                    })
                    # Commit the transaction after each record creation
                    product_ppn_model.env.cr.commit()
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Product PPN')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_product_ppn&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_product_ppn')
        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/product/ppn')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
        
    # product dinkes
    @http.route('/import/product/dinkes', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product_dinkes(self, **kwargs):
        product_dinkes_model = request.env['product.barang.dinkes'].sudo()
        _logger.info("Import Provinsi function called")

        try:
            # Fetch data from the external service
            url = "http://192.168.16.130/microservice_internal/produk/produk/getBarangDinkes/"
            response = requests.get(url)
            
            # Check if the response is successful
            if response.status_code != 200:
                return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)

            data = response.json()

            # Process each item in the received data
            for item in data.get('data', []):
                existing_provinsi = product_dinkes_model.search([('kode_barang_dinkes', '=', item.get('kode_barang_dinkes'))])
                if not existing_provinsi:
                    product_dinkes_model.with_context(skip_external_api=True).create({
                        'kode_barang_dinkes': item.get('kode_barang_dinkes'),
                        'nama_barang_dinkes': item.get('nama_barang_dinkes'),
                    })
                    # Commit the transaction after each record creation
                    product_dinkes_model.env.cr.commit()
            # return "Data import successful"
            # return request.redirect('/web#action=inventory_bsp.action_wilayah_provinsi')
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Product Barang Dinkes')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_product_barang_dinkes&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_product_barang_dinkes')
        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/product/dinkes')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})
        
    # product konversi
    @http.route('/import/product/konversi', type='http', auth='user', methods=['GET'], website=True, csrf=False)
    def import_product_konversi(self, **kwargs):
        product_konversi_model = request.env['product.konversi'].sudo()
        _logger.info("Import Provinsi function called")

        # Define the list of type_konversi to iterate
        types_konversi = ['barang_satuan', 'barang_cabang', 'barang_outlet']

        try:
            # Iterate over each type_konversi
            url = "http://192.168.16.130/microservice_internal/produk/produk/getHargaBarangKonversi?type_konversi=barang_satuan"
            response = requests.get(url)

            # Check if the response is successful
            if response.status_code == 201 or response.status_code == 200:
                # return "Cannot fetch data from the given URL. Status code: {}".format(response.status_code)
                data = response.json()
                # Process each item in the received data
                for item in data.get('data', []):
                    existing_provinsi = product_konversi_model.search([('kode_harga_konversi', '=', item.get('kode_harga_konversi'))])
                    if not existing_provinsi:
                        kode_cabang = request.env['res.company'].search([
                            ('kode_cabang', '=', item.get('kode_cabang'))
                        ], limit=1)
                        kode_barang = request.env['product.template'].search([
                            ('kode_barang', '=', item.get('kode_barang'))
                        ], limit=1)
                        product_konversi_model.with_context(skip_external_api=True).create({
                            'kode_harga_konversi': item.get('kode_harga_konversi'),
                            'kode_barang_id': kode_barang.id if kode_barang else False,
                            'kategori_penjualan_barang': item.get('kategori_penjualan_barang'),
                            'level': item.get('level'),
                            'konversi_satuan': item.get('konversi_satuan'),
                            'jual_satuan': item.get('jual_satuan'),
                            'return_satuan': item.get('return_satuan'),
                            'spreading_satuan': item.get('spreading_satuan'),
                            'berat_satuan': item.get('berat_satuan'),
                            'panjang_satuan': item.get('panjang_satuan'),
                            'lebar_satuan': item.get('lebar_satuan'),
                            'tinggi_satuan': item.get('tinggi_satuan'),
                            'harga_beli': item.get('harga_beli'),
                            'harga_tac': item.get('harga_tac'),
                            'harga_jual': item.get('harga_jual'),
                            'harga_speading': item.get('harga_speading'),
                            'kode_cabang_id': kode_cabang.id if kode_cabang else False,
                            'kode_jenis_outlet': item.get('kode_jenis_outlet'),
                            'satuan_level': item.get('satuan_level'),
                            'nama_barang': item.get('nama_barang'),
                        })
                        # Commit the transaction after each record creation
                        product_konversi_model.env.cr.commit()
            url2 = "http://192.168.16.130/microservice_internal/produk/produk/getHargaBarangKonversi?type_konversi=barang_cabang"
            response2 = requests.get(url2)
            # Check if the response is successful
            if response2.status_code == 201 or response2.status_code == 200:
                # return "Cannot fetch data from the given URL. Status code: {}".format(response2.status_code)
                data = response2.json()
                # Process each item in the received data
                for item in data.get('data', []):
                    existing_provinsi = product_konversi_model.search([('kode_harga_konversi', '=', item.get('kode_harga_konversi'))])
                    if not existing_provinsi:
                        kode_cabang = request.env['res.company'].search([
                            ('kode_cabang', '=', item.get('kode_cabang'))
                        ], limit=1)
                        kode_barang = request.env['product.template'].search([
                            ('kode_barang', '=', item.get('kode_barang'))
                        ], limit=1)
                        product_konversi_model.with_context(skip_external_api=True).create({
                            'kode_harga_konversi': item.get('kode_harga_konversi'),
                            'kode_barang_id': kode_barang.id if kode_barang else False,
                            'kategori_penjualan_barang': item.get('kategori_penjualan_barang'),
                            'level': item.get('level'),
                            'konversi_satuan': item.get('konversi_satuan'),
                            'jual_satuan': item.get('jual_satuan'),
                            'return_satuan': item.get('return_satuan'),
                            'spreading_satuan': item.get('spreading_satuan'),
                            'berat_satuan': item.get('berat_satuan'),
                            'panjang_satuan': item.get('panjang_satuan'),
                            'lebar_satuan': item.get('lebar_satuan'),
                            'tinggi_satuan': item.get('tinggi_satuan'),
                            'harga_beli': item.get('harga_beli'),
                            'harga_tac': item.get('harga_tac'),
                            'harga_jual': item.get('harga_jual'),
                            'harga_speading': item.get('harga_speading'),
                            'kode_cabang_id': kode_cabang.id if kode_cabang else False,
                            'kode_jenis_outlet': item.get('kode_jenis_outlet'),
                            'satuan_level': item.get('satuan_level'),
                            'nama_barang': item.get('nama_barang'),
                        })
                        # Commit the transaction after each record creation
                        product_konversi_model.env.cr.commit()
            url3 = "http://192.168.16.130/microservice_internal/produk/produk/getHargaBarangKonversi?type_konversi=barang_outlet"
            response3 = requests.get(url3)
            # Check if the response is successful
            if response3.status_code == 201 or response3.status_code == 200:
                # return "Cannot fetch data from the given URL. Status code: {}".format(response3.status_code)
                data = response3.json()
                # Process each item in the received data
                for item in data.get('data', []):
                    existing_provinsi = product_konversi_model.search([('kode_harga_konversi', '=', item.get('kode_harga_konversi'))])
                    if not existing_provinsi:
                        kode_cabang = request.env['res.company'].search([
                            ('kode_cabang', '=', item.get('kode_cabang'))
                        ], limit=1)
                        kode_barang = request.env['product.template'].search([
                            ('kode_barang', '=', item.get('kode_barang'))
                        ], limit=1)
                        product_konversi_model.with_context(skip_external_api=True).create({
                            'kode_harga_konversi': item.get('kode_harga_konversi'),
                            'kode_barang_id': kode_barang.id if kode_barang else False,
                            'kategori_penjualan_barang': item.get('kategori_penjualan_barang'),
                            'level': item.get('level'),
                            'konversi_satuan': item.get('konversi_satuan'),
                            'jual_satuan': item.get('jual_satuan'),
                            'return_satuan': item.get('return_satuan'),
                            'spreading_satuan': item.get('spreading_satuan'),
                            'berat_satuan': item.get('berat_satuan'),
                            'panjang_satuan': item.get('panjang_satuan'),
                            'lebar_satuan': item.get('lebar_satuan'),
                            'tinggi_satuan': item.get('tinggi_satuan'),
                            'harga_beli': item.get('harga_beli'),
                            'harga_tac': item.get('harga_tac'),
                            'harga_jual': item.get('harga_jual'),
                            'harga_speading': item.get('harga_speading'),
                            'kode_cabang_id': kode_cabang.id if kode_cabang else False,
                            'kode_jenis_outlet': item.get('kode_jenis_outlet'),
                            'satuan_level': item.get('satuan_level'),
                            'nama_barang': item.get('nama_barang'),
                        })
                        # Commit the transaction after each record creation
                        product_konversi_model.env.cr.commit()
            
            menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Product Konversi')], limit=1)
            menu_id = menu.id if menu else None

            # Construct the redirection URL with the dynamically found menu ID
            if menu_id:
                return request.redirect(f'/web#action=inventory_bsp.action_product_konversi&menu_id={menu_id}')
            else:
                return request.redirect('/web#action=inventory_bsp.action_product_konversi')
        except requests.exceptions.RequestException as e:
            # Check if the error message is the specific connection aborted message
            if "Connection aborted" in str(e) and "RemoteDisconnected" in str(e):
                # Redirect to the same page or a specific page to refresh
                return request.redirect(f'/import/product/konversi')
            else:
                # Return the error message for other types of exceptions
                return json.dumps({'error': str(e)})