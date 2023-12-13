from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ProductPpn(models.Model):

    _name = 'product.ppn'

    kode_barang_ppn = fields.Char()  
    kode_barang_id = fields.Many2one('product.template', string='Kode Barang', context={'show_kode_barang': True})
    tanggal_mulai_berlaku = fields.Date()
    PPN = fields.Char()
    bebas_ppn = fields.Char()
    tanggal_berakhir_ppn = fields.Date()

    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating product.categories with vals: %s", vals)
        # record = self.env['product.categories'].create(vals)
        record = super(ProductPpn, self).create(vals)
        self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        data_to_send = {
            'kode_barang_ppn': record.kode_barang_ppn,
            'kode_barang': record.kode_barang_id.kode_barang if record.kode_barang_id else None,
            'tanggal_mulai_berlaku': record.tanggal_mulai_berlaku.isoformat() if record.tanggal_mulai_berlaku else None,
            'PPN': record.PPN,
            'bebas_ppn': record.bebas_ppn,
            'tanggal_berakhir_ppn': record.tanggal_berakhir_ppn.isoformat() if record.tanggal_berakhir_ppn else None
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/produk/addPpnProduk/",
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
        result = super(ProductPpn, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            formatted_tanggal_mulai_berlaku = record.tanggal_mulai_berlaku.strftime("%Y-%m-%d") if record.tanggal_mulai_berlaku else None
            formatted_tanggal_berakhir_ppn = record.tanggal_berakhir_ppn.strftime("%Y-%m-%d") if record.tanggal_berakhir_ppn else None

            data_to_send = {
                'kode_barang_ppn': record.kode_barang_ppn,
                'kode_barang': record.kode_barang_id.kode_barang if record.kode_barang_id else None,
                'tanggal_berakhir_ppn': formatted_tanggal_mulai_berlaku,
                'PPN': vals.get('PPN', record.PPN),
                'bebas_ppn': vals.get('bebas_ppn', record.bebas_ppn),
                'tanggal_berakhir_ppn': formatted_tanggal_berakhir_ppn
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)

            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/produk/updatePpnProduk/",
                    json=data_to_send,
                    headers=headers
                )
                if response.status_code == 200:
                    _logger.info("Success: Data updated to external API. Response: %s", response.json())
                else:
                    _logger.error("Failed to send update to external API. Status Code: %s, Response: %s",
                                  response.status_code, response.text)
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
        return super(ProductPpn, self).unlink()
    
    def delete_from_external_api(self, record):
        data_to_send = {
            'kode_barang_ppn': record.kode_barang_ppn
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.delete(
                "http://192.168.16.130/microservice_internal/produk/produk/deletePpnProduk/",
                json=data_to_send,
                headers=headers
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Gagal menghapus data dari API eksternal: %s", e)
            raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

        _logger.info("Sukses: Data dihapus dari API eksternal.")

    