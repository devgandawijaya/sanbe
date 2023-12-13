from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ProductDivisi(models.Model):

    _name = 'product.divisi'
    _rec_name = 'kode_divisi_produk'


    kode_divisi_produk = fields.Char()  
    partner_id = fields.Many2one('res.partner', string='Vendor')
    kode_prinsipal = fields.Char(related="partner_id.kode_principal", string='Kode vendor')
    # kode_prinsipale_id = fields.Many2one('res.partner', string='Kode Vendor', context={'show_kode_principal': True})
    nama_divisi_produk = fields.Char()
    na_divisi_produk = fields.Char()
    karyawan_id = fields.Many2one(
        'res.users', 
        string='Nama Karyawan', 
        default=lambda self: self.env.uid
    )
    exclusive = fields.Char()
    vaccine = fields.Char()
    time_stime = fields.Datetime()
    
    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating product.categories with vals: %s", vals)
        # record = self.env['product.categories'].create(vals)
        record = super(ProductDivisi, self).create(vals)
        self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        payload = {
            'kode_divisi_produk': record.kode_divisi_produk,
            'kode_prinsipale': record.kode_prinsipal,
            'nama_divisi_produk': record.nama_divisi_produk,
            'na_divisi_produk': record.na_divisi_produk,
            'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
            'exclusive': record.exclusive,
            'vaccine': record.vaccine,
            'time_stime': record.time_stime.isoformat() if record.time_stime else None
        }
        _logger.info("Payload to send to external API: %s", payload)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/produk/addDivisiProduk/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status() 
        except requests.exceptions.HTTPError as e:
            _logger.error("HTTP Error: %s", e.response.text)
            raise UserError('HTTP Error: {}'.format(e.response.text))
        except requests.exceptions.RequestException as e:
            _logger.error("Failed to send data to external API: %s", e)
            if e.response:
                _logger.error("Response Status Code: %s Response Text: %s", e.response.status_code, e.response.text)
            raise UserError('Failed to send data to external API: {}'.format(e))




    # update/put data
    def write(self, vals):
        result = super(ProductDivisi, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            formatted_time_stime = record.time_stime.strftime("%Y-%m-%d %H:%M:%S") if record.time_stime else None

            data_to_send = {
                'kode_divisi_produk': record.kode_divisi_produk,
                'kode_prinsipale': vals.get('kode_prinsipal', record.kode_prinsipal),
                'nama_divisi_produk': vals.get('nama_divisi_produk', record.nama_divisi_produk),
                'na_divisi_produk': vals.get('na_divisi_produk', record.na_divisi_produk),
                'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
                'exclusive': vals.get('exclusive', record.exclusive),
                'vaccine': vals.get('vaccine', record.vaccine),
                'time_stime': formatted_time_stime
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)

            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/produk/updateDivisiProduk/",
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

    # def unlink(self):
    #     for record in self:
    #         self.delete_from_external_api(record)
    #     return super(ProductDivisi, self).unlink()
    
    # def delete_from_external_api(self, record):
    #     data_to_send = {
    #         'kode_divisi_produk': record.kode_divisi_produk
    #     }
    #     headers = {'Content-Type': 'application/json'}
    #     try:
    #         response = requests.delete(
    #             "http://192.168.16.130/microservice_internal/produk/produk/deleteDivisiProduk/",
    #             json=data_to_send,
    #             headers=headers
    #         )
    #         response.raise_for_status() 
    #     except requests.exceptions.RequestException as e:
    #         _logger.error("Gagal menghapus data dari API eksternal: %s", e)
    #         raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

    #     _logger.info("Sukses: Data dihapus dari API eksternal.")

    