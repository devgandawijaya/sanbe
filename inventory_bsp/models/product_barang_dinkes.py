from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ProductBarangDinkes(models.Model):

    _name = 'product.barang.dinkes'
    _rec_name = 'kode_barang_dinkes'

    kode_barang_dinkes = fields.Char() 
    nama_barang_dinkes = fields.Char()

    def action_import_barang_dinkes(self):
        url = "http://192.168.16.130/microservice_internal/produk/produk/getBarangDinkes/"
        response = requests.get(url)
        if response.status_code != 200:
            raise UserError('Cannot fetch data from the given URL.')

        data = response.json()
        for item in data.get('data', []):
            existing_category = self.search([('kode_barang_dinkes', '=', item.get('kode_barang_dinkes'))])
            if existing_category:
                # _logger.info("Category with code %s already exists. Skipping.", item.get('kode_barang_dinkes'))
                continue
            self.with_context(skip_external_api=True).create({
                'kode_barang_dinkes': item.get('kode_barang_dinkes'),
                'nama_barang_dinkes': item.get('nama_barang_dinkes'),
            })
            
     # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating prinsipal.channel with vals: %s", vals)
        record = super(ProductBarangDinkes, self).create(vals)
        if not self.env.context.get('skip_external_api', False):
            self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        data_to_send = {
            'kode_barang_dinkes': record.kode_barang_dinkes,
            'nama_barang_dinkes': record.nama_barang_dinkes,
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/produk/addBarangDinkes/",
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
        result = super(ProductBarangDinkes, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            data_to_send = {
                'kode_barang_dinkes': record.kode_barang_dinkes,
                'nama_barang_dinkes': vals.get('nama_barang_dinkes', record.nama_barang_dinkes),
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)

            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/produk/updateBarangDinkes/",
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
                    raise UserError('Failed to send update to external API. Status Code: {}, Response: {}'.format(response.status_code, response.text))
            except requests.exceptions.RequestException as e:
                _logger.error("Failed to send update to external API: %s", e)
                _logger.debug("Request Data: %s", data_to_send)
                _logger.debug("Headers: %s", headers)
                _logger.debug("Exception: %s", e.__dict__)
                raise UserError('Failed to send update to external API: {}'.format(e))

    def unlink(self):
        for record in self:
            self.delete_from_external_api(record)
        return super(ProductBarangDinkes, self).unlink()
    
    def delete_from_external_api(self, record):
        data_to_send = {
            'kode_barang_dinkes': record.kode_barang_dinkes
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.delete(
                "http://192.168.16.130/microservice_internal/produk/produk/deleteBarangDinkes/",
                json=data_to_send,
                headers=headers
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Gagal menghapus data dari API eksternal: %s", e)
            raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

        _logger.info("Sukses: Data dihapus dari API eksternal.")
