from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ProductKonversi(models.Model):

    _name = 'product.konversi'  

    kode_harga_konversi = fields.Char()
    kode_barang_id = fields.Many2one('product.template', string='Kode Barang', context={'show_kode_barang': True})
    kategori_penjualan_barang = fields.Selection([
        ('barang_satuan', 'Barang Satuan'), 
        ('barang_cabang', 'Barang Cabang'),
        ('barang_outlet', 'Barang Outlet')
    ])

    level = fields.Char()
    konversi_satuan = fields.Char()
    jual_satuan = fields.Char()
    return_satuan = fields.Char()
    spreading_satuan = fields.Char()
    berat_satuan = fields.Char()
    panjang_satuan = fields.Char()
    lebar_satuan = fields.Char()
    tinggi_satuan = fields.Char()
    harga_beli = fields.Float()
    harga_tac = fields.Float()
    harga_jual = fields.Float()
    harga_speading = fields.Float()
    kode_cabang_id = fields.Many2one('res.company', string='Kode Cabang', context={'show_kode_cabang': True})
    kode_jenis_outlet = fields.Char()
    satuan_level = fields.Char()
    nama_barang = fields.Char(related='kode_barang_id.name', readonly=True, store=True)

    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating product.categories with vals: %s", vals)
        record = super(ProductKonversi, self).create(vals)
        if not self.env.context.get('skip_external_api', False):
            self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        data_to_send = {
            'kode_harga_konversi': record.kode_harga_konversi,
            'kode_barang': record.kode_barang_id.kode_barang if record.kode_barang_id else None,
            'kategori_penjualan_barang': record.kategori_penjualan_barang,
            'level': record.level,
            'konversi_satuan': record.konversi_satuan,
            'jual_satuan': record.jual_satuan,
            'return_satuan': record.return_satuan,
            'spreading_satuan': record.spreading_satuan,
            'berat_satuan': record.berat_satuan,
            'panjang_satuan': record.panjang_satuan,
            'lebar_satuan': record.lebar_satuan,
            'tinggi_satuan': record.tinggi_satuan,
            'harga_beli': record.harga_beli,
            'harga_tac': record.harga_tac,
            'harga_jual': record.harga_jual,
            'harga_speading': record.harga_speading,
            'kode_cabang': record.kode_cabang_id.kode_cabang if record.kode_cabang_id else None,
            'kode_jenis_outlet': record.kode_jenis_outlet,
            'satuan_level': record.satuan_level,
            'nama_barang': record.nama_barang,
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/produk/addHargaBarangKonversi/",
                json=data_to_send,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Failed to send data to external API: %s", e)
            raise UserError('Failed to send data to external API: {}'.format(e))

        _logger.info("Success: Data sent to external API.")

    # update/put data
    def write(self, vals):
        result = super(ProductKonversi, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            data_to_send = {
                'kode_harga_konversi': record.kode_harga_konversi,
                'kode_barang': record.kode_barang_id.kode_barang if record.kode_barang_id else None,
                'kategori_penjualan_barang': vals.get('kategori_penjualan_barang', record.kategori_penjualan_barang),
                'level': vals.get('level', record.level),
                'konversi_satuan': vals.get('konversi_satuan', record.konversi_satuan),
                'jual_satuan': vals.get('jual_satuan', record.jual_satuan),
                'return_satuan': vals.get('return_satuan', record.return_satuan),
                'spreading_satuan': vals.get('spreading_satuan', record.spreading_satuan),
                'berat_satuan': vals.get('berat_satuan', record.berat_satuan),
                'panjang_satuan': vals.get('panjang_satuan', record.panjang_satuan),
                'lebar_satuan': vals.get('lebar_satuan', record.lebar_satuan),
                'tinggi_satuan': vals.get('tinggi_satuan', record.tinggi_satuan),
                'harga_beli': vals.get('harga_beli', record.harga_beli),
                'harga_tac': vals.get('harga_tac', record.harga_tac),
                'harga_jual': vals.get('harga_jual', record.harga_jual),
                'harga_speading': vals.get('harga_speading', record.harga_speading),
                'kode_cabang': record.kode_cabang_id.kode_cabang if record.kode_cabang_id else None,
                'kode_jenis_outlet': vals.get('kode_jenis_outlet', record.kode_jenis_outlet),
                'satuan_level': vals.get('satuan_level', record.satuan_level),
                'nama_barang': vals.get('nama_barang', record.nama_barang),
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)

            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/produk/updateKelompokProduk/",
                    json=data_to_send,
                    headers=headers
                )
                if response.status_code == 200:
                    _logger.info("Success: Data updated to external API. Response: %s", response.json())
                else:
                    _logger.error("Failed to send update to external API. Status Code: %s, Response: %s",response.status_code, response.text)
                    _logger.debug("Request Data: %s", data_to_send)
                    _logger.debug("Headers: %s", headers)
                    _logger.debug("Full Response: %s", response.__dict__)
                    raise UserError('Failed to send update to external API. Status Code: {}, Response: {}'.format(
                        response.status_code, response.text))
            except requests.exceptions.RequestException as e:
                _logger.error("Failed to send update to external API: %s", e)
                _logger.debug("Request Data: %s", data_to_send)
                _logger.debug("Headers: %s", headers)
                _logger.debug("Exception: %s", e.__dict__)
                raise UserError('Failed to send update to external API: {}'.format(e))
            
    def unlink(self):
        for record in self:
            self.delete_from_external_api(record)
        return super(ProductKonversi, self).unlink()
    
    def delete_from_external_api(self, record):
        data_to_send = {
            'kode_harga_konversi': record.kode_harga_konversi,
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.delete(
                "http://192.168.16.130/microservice_internal/produk/produk/deleteHargaBarangKonversi/",
                json=data_to_send,
                headers=headers
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Gagal menghapus data dari API eksternal: %s", e)
            raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

        _logger.info("Sukses: Data dihapus dari API eksternal.")