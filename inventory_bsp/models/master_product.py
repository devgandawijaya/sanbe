from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import json
import requests
import logging

_logger = logging.getLogger(__name__)

class MasterProduct(models.Model):
    _inherit = 'product.template'

    kode_barang = fields.Char()
    kode_kelompok_barang = fields.Char(related='nama_kelompok_barang_id.kode_kelompok_barang', readonly=True)
    nama_kelompok_barang_id = fields.Many2one('product.kelompok',string='Nama Kelompok Barang')
    kode_divisi_produk_id = fields.Many2one('product.divisi',string='Kode Produk Divisi')
    nama_divisi_produk = fields.Char(related='kode_divisi_produk_id.nama_divisi_produk', readonly=True)
    kode_barang_dinkes_id = fields.Many2one('product.barang.dinkes',string='Kode Barang Dinkes')
    kode_register_obat_id = fields.Many2one('product.registrasi.obat',string='Kode Registrasi Obat')
    kode_kategori_barang = fields.Char(related='nama_kategori_id.kode_kategori_barang', readonly=True)
    nama_kategori_id = fields.Many2one('product.category',string='Nama Kategori')
    nama_barang = fields.Char()
    harga_jual = fields.Float()
    harga_beli = fields.Float()
    harga_tac = fields.Float()
    harga_spreading = fields.Integer()
    tanggal_discontinue = fields.Datetime()
    std_lead_time = fields.Integer()
    pengali = fields.Char()
    tempo = fields.Integer()
    purchasing_level = fields.Char()
    # karyawan_id = fields.Many2one('hr.employee', string='Nama Karyawan')
    karyawan_id = fields.Many2one(
        'res.users', 
        string='Nama Karyawan', 
        default=lambda self: self.env.uid
    )
    time_stamp = fields.Datetime()
    is_directly_updated = fields.Boolean(default=False)
    def name_get(self):
        if self.env.context.get('show_kode_barang'):
            return [(record.id, record.kode_barang) for record in self]
        else:
            return [(record.id, record.name) for record in self]

    @api.onchange('harga_jual')
    def _onchange_harga_jual(self):
        if self.harga_jual:
            self.list_price = self.harga_jual

    @api.onchange('list_price')
    def _onchange_list_price(self):
        if self.list_price:
            self.standard_price = self.list_price


    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating product.categories with vals: %s", vals)
        record = super(MasterProduct, self).create(vals)
        if not self.env.context.get('skip_external_api', False):
            self.post_to_external_api(record)
        return record
    def post_to_external_api(self, record):
        data_to_send = {
            'kode_barang': record.kode_barang,
            'kode_kelompok_barang': record.kode_kelompok_barang,
            'nama_kelompok_barang': record.nama_kelompok_barang_id.nama_kelompok_barang if record.nama_kelompok_barang_id else None,
            'kode_divisi_produk': record.kode_divisi_produk_id.kode_divisi_produk if record.kode_divisi_produk_id else None,
            'nama_divisi_produk': record.nama_divisi_produk,
            'kode_barang_dinkes': record.kode_barang_dinkes_id.kode_barang_dinkes if record.kode_barang_dinkes_id else None,
            'kode_register_obat': record.kode_register_obat_id.name if record.kode_register_obat_id else None,
            'kode_kategori_barang': record.kode_kategori_barang,
            'nama_kategori': record.nama_kategori_id.name if record.nama_kategori_id else None,
            'nama_barang': record.name,
            'harga_jual': record.harga_jual,
            'harga_beli': record.harga_beli,
            'harga_tac': record.harga_tac,
            'harga_spreading': record.harga_spreading,
            'tanggal_discontinue': record.tanggal_discontinue.isoformat() if record.tanggal_discontinue else None,
            'std_lead_time': record.std_lead_time,
            'pengali': record.pengali,
            'tempo': record.tempo,
            'purchasing_level': record.purchasing_level,
            'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
            'time_stamp': record.time_stamp.isoformat() if record.time_stamp else None
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/produk/addProduk",
                json=data_to_send,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Failed to send data to external API: %s", e)
            raise UserError('Failed to send data to external API: {}'.format(e))

        _logger.info("Success: Data sent to external API.")


    def write(self, vals):
        result = super(MasterProduct, self).write(vals)
        if not self.env.context.get('skip_external_api_update', False):
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            formatted_tanggal_discontinue = record.tanggal_discontinue.strftime("%Y-%m-%d %H:%M:%S") if record.tanggal_discontinue else None
            formatted_time_stamp = record.time_stamp.strftime("%Y-%m-%d %H:%M:%S") if record.time_stamp else None
            data_to_send = {
                'kode_barang': record.kode_barang,
                'kode_kelompok_barang': vals.get('kode_kelompok_barang', record.kode_kelompok_barang),
                'nama_kelompok_barang': record.nama_kelompok_barang_id.nama_kelompok_barang if record.nama_kelompok_barang_id else None,
                'kode_divisi_produk': record.kode_divisi_produk_id.kode_divisi_produk if record.kode_divisi_produk_id else None,
                'nama_divisi_produk': vals.get('nama_divisi_produk', record.nama_divisi_produk),
                'kode_barang_dinkes': record.kode_barang_dinkes_id.kode_barang_dinkes if record.kode_barang_dinkes_id else None,
                'kode_register_obat': record.kode_register_obat_id.name if record.kode_register_obat_id else None,
                'kode_kategori_barang': vals.get('kode_kategori_barang', record.kode_kategori_barang),
                'nama_kategori': record.nama_kategori_id.name if record.nama_kategori_id else None,
                'nama_barang': vals.get('name', record.name),
                'harga_jual': vals.get('harga_jual', record.harga_jual),
                'harga_beli': vals.get('harga_beli', record.harga_beli),
                'harga_tac': vals.get('harga_tac', record.harga_tac),
                'harga_spreading': vals.get('harga_spreading', record.harga_spreading),
                'tanggal_discontinue': formatted_tanggal_discontinue,
                'std_lead_time': vals.get('std_lead_time', record.std_lead_time),
                'pengali': vals.get('pengali', record.pengali),
                'tempo': vals.get('tempo', record.tempo),
                'purchasing_level': vals.get('purchasing_level', record.purchasing_level),
                'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
                'time_stamp': formatted_time_stamp if formatted_time_stamp else None
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/produk/updateProduk",
                    json=data_to_send,
                    headers=headers
                )
                if response.status_code == 200:
                    try:
                        response_data = response.json() 
                        _logger.info("Success: Data updated to external API. Response: %s", response_data)
                    except json.JSONDecodeError:
                        _logger.error("Received non-JSON response: %s", response.text)
                        # Opsional: Tambahkan lebih banyak logika penanganan di sini
                        raise UserError("Received non-JSON response from external API.")
                else:
                    _logger.error("Failed to send update to external API. Status Code: %s, Response: %s", response.status_code, response.text)
                    # Opsional: Tambahkan lebih banyak logika penanganan di sini
                    raise UserError('Failed to send update to external API. Status Code: {}, Response: {}'.format(response.status_code, response.text))
            except requests.exceptions.ConnectionError as e:
                _logger.error("Connection error while sending update to external API: %s", e)
                raise UserError('Connection error while sending update to external API: {}'.format(e))
            except requests.exceptions.RequestException as e:
                _logger.error("Failed to send update to external API: %s", e)
                raise UserError('Failed to send update to external API: {}'.format(e))
            
    # def unlink(self):
    #     for record in self:
    #         self.delete_from_external_api(record)
    #     return super(MasterProduct, self).unlink()
    
    # def delete_from_external_api(self, record):
    #     data_to_send = {
    #         'kode_barang': record.kode_barang
    #     }
    #     headers = {'Content-Type': 'application/json'}
    #     try:
    #         response = requests.delete(
    #             "http://192.168.16.130/microservice_internal/produk/produk/deleteProduk",
    #             json=data_to_send,
    #             headers=headers
    #         )
    #         response.raise_for_status() 
    #     except requests.exceptions.RequestException as e:
    #         _logger.error("Gagal menghapus data dari API eksternal: %s", e)
    #         raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

    #     _logger.info("Sukses: Data dihapus dari API eksternal.")

    
class CustomPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        # Pertama, panggil implementasi asli dari button_confirm
        res = super(CustomPurchaseOrder, self).button_confirm()

        # Contoh pemanggilan write dengan konteks tambahan
        product_template_ids = self.mapped('order_line.product_id.product_tmpl_id')
        for template in product_template_ids:
            template.with_context(skip_update_to_external_api=True).write({})

        return res
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_id:
                product_template = record.product_id.product_tmpl_id
                record.price_unit = product_template.list_price
                _logger.info(f'Product ID: {record.product_id.id}, Price Unit set to: {record.price_unit}')

    @api.onchange('product_qty')
    def _onchange_product_qty(self):
        if self.product_id and self.price_unit == 0.0:
            product_template = self.product_id.product_tmpl_id
            self.price_unit = product_template.list_price
            _logger.info(f'Product Qty changed for Product ID: {self.product_id.id}, Price Unit reset to: {self.price_unit}')