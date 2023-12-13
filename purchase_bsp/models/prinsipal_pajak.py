from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class prinsipalPajak(models.Model):

    _name = 'prinsipal.pajak'

    kode_pajak_prinsipal = fields.Char()
    kode_principal = fields.Char(related='nama_principal_id.name', readonly=True, store=True)
    tanggal_pengajuan = fields.Date()
    status_pajak = fields.Char()
    karyawan_id = fields.Many2one(
        'res.users', 
        string='Nama Karyawan', 
        default=lambda self: self.env.uid
    )
    time_stamp = fields.Date()
    time_create = fields.Date()
    nama_principal_id = fields.Many2one('res.partner', string='Nama Vendor')


    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating prinsipal.channel with vals: %s", vals)
        record = super(prinsipalPajak, self).create(vals)
        if not self.env.context.get('skip_external_api', False):
            self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        data_to_send = {
            'kode_pajak_prinsipal': record.kode_pajak_prinsipal,
            'kode_principal': record.kode_principal,
            'tanggal_pengajuan': record.tanggal_pengajuan.isoformat() if record.tanggal_pengajuan else None,
            'status_pajak': record.status_pajak,
            'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
            'time_stamp': record.time_stamp.isoformat() if record.time_stamp else None,
            'time_create':record.time_create.isoformat() if record.time_create else None,
            'nama_principal': record.nama_principal_id.name if record.nama_principal_id else None,
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/Prinsipal/addPrinsipalPajak",
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
        result = super(prinsipalPajak, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            formatted_tanggal_pengajuan = record.tanggal_pengajuan.strftime("%Y-%m-%d") if record.tanggal_pengajuan else None
            formatted_time_stamp = record.time_stamp.strftime("%Y-%m-%d") if record.time_stamp else None
            formatted_time_create = record.time_create.strftime("%Y-%m-%d") if record.time_create else None
            data_to_send = {
                'kode_pajak_prinsipal': record.kode_pajak_prinsipal,
                'kode_principal': vals.get('kode_principal', record.kode_principal),
                'tanggal_pengajuan': formatted_tanggal_pengajuan if formatted_tanggal_pengajuan else None,
                'status_pajak': vals.get('status_pajak', record.status_pajak),
                'karyawan_id': record.karyawan_id.name if record.karyawan_id else None,
                'time_stamp': formatted_time_stamp if formatted_time_stamp else None,
                'time_create': formatted_time_create if formatted_time_create else None,
                'nama_principal_id': record.nama_principal_id.name if record.nama_principal_id else None,
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/Prinsipal/updatePrinsipalPajak",
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
        return super(prinsipalPajak, self).unlink()
    
    def delete_from_external_api(self, record):
        data_to_send = {
            'kode_pajak_prinsipal': record.kode_pajak_prinsipal
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.delete(
                "http://192.168.16.130/microservice_internal/produk/Prinsipal/deletePrinsipalPajak",
                json=data_to_send,
                headers=headers
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Gagal menghapus data dari API eksternal: %s", e)
            raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

        _logger.info("Sukses: Data dihapus dari API eksternal.")

    