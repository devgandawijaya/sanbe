from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class prinsipal(models.Model):

    _name = 'prinsipal.master'

    kode_principal = fields.Char()
    nama_principal = fields.Char()
    cp_logistik = fields.Char()
    cp_finance = fields.Char()
    cp_marketing = fields.Char()
    tlp_principal = fields.Char()
    fax_principal = fields.Char()
    alamat_principal = fields.Char()
    email_principal = fields.Char()
    npwp_principal = fields.Char()
    tanggal_bergabung = fields.Date()
    tanggal_berhenti = fields.Date()
    jenis_pengembalian = fields.Char()
    percent_pembulatan = fields.Char()
    disonfaktur = fields.Char()
    faktur_eklusif = fields.Char()
    eklusif_awal = fields.Date()
    eklusif_akhir = fields.Date()
    nama_bm = fields.Char()
    id_karyawan = fields.Char()
    time_stamp = fields.Date()
    harga_acuan = fields.Char()
    nomor_nppkp = fields.Char()
    tgl_pkp = fields.Date()
    mata_uang = fields.Char()


    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating product.categories with vals: %s", vals)
        # record = self.env['product.categories'].create(vals)
        record = super(prinsipal, self).create(vals)
        self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        data_to_send = {
            'kode_principal': record.kode_principal,
            'nama_principal': record.nama_principal,
            'cp_logistik': record.cp_logistik,
            'cp_finance': record.cp_finance,
            'cp_marketing': record.cp_marketing,
            'tlp_principal': record.tlp_principal,
            'fax_principal': record.fax_principal,
            'alamat_principal': record.alamat_principal,
            'email_principal': record.email_principal,
            'npwp_principal': record.npwp_principal,
            'tanggal_bergabung': record.tanggal_bergabung.isoformat() if record.tanggal_bergabung else None,
            'tanggal_berhenti': record.tanggal_berhenti.isoformat() if record.tanggal_berhenti else None,
            'jenis_pengembalian': record.jenis_pengembalian,
            'percent_pembulatan': record.percent_pembulatan,
            'disonfaktur': record.disonfaktur,
            'faktur_eklusif': record.faktur_eklusif,
            'eklusif_awal': record.eklusif_awal.isoformat() if record.eklusif_awal else None,
            'eklusif_akhir': record.eklusif_akhir.isoformat() if record.eklusif_akhir else None,
            'nama_bm': record.nama_bm,
            'id_karyawan': record.id_karyawan,
            'time_stamp': record.time_stamp.isoformat() if record.time_stamp else None,
            'harga_acuan': record.harga_acuan,
            'nomor_nppkp': record.nomor_nppkp,
            'tgl_pkp': record.tgl_pkp.isoformat() if record.tgl_pkp else None,
            'mata_uang': record.mata_uang,
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/Prinsipal/addPrinsipal",
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
        result = super(prinsipal, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            formatted_tanggal_bergabung = record.tanggal_bergabung.strftime("%Y-%m-%d") if record.tanggal_bergabung else None
            formatted_tanggal_berhenti = record.tanggal_berhenti.strftime("%Y-%m-%d") if record.tanggal_berhenti else None
            formatted_eklusif_awal = record.eklusif_awal.strftime("%Y-%m-%d") if record.eklusif_awal else None
            formatted_eklusif_akhir = record.eklusif_akhir.strftime("%Y-%m-%d") if record.eklusif_akhir else None
            formatted_time_stamp = record.time_stamp.strftime("%Y-%m-%d") if record.time_stamp else None
            formatted_tgl_pkp = record.tgl_pkp.strftime("%Y-%m-%d") if record.tgl_pkp else None

            data_to_send = {
                'kode_principal': record.kode_principal,
                'nama_principal': vals.get('nama_principal', record.nama_principal),
                'cp_logistik': vals.get('cp_logistik', record.cp_logistik),
                'cp_finance': vals.get('cp_finance', record.cp_finance),
                'cp_marketing': vals.get('cp_marketing', record.cp_marketing),
                'tlp_principal': vals.get('tlp_principal', record.tlp_principal),
                'fax_principal': vals.get('fax_principal', record.fax_principal),
                'alamat_principal': vals.get('alamat_principal', record.alamat_principal),
                'email_principal': vals.get('email_principal', record.email_principal),
                'npwp_principal': vals.get('npwp_principal', record.npwp_principal),
                'tanggal_bergabung': formatted_tanggal_bergabung,
                'tanggal_berhenti': formatted_tanggal_berhenti,
                'jenis_pengembalian': vals.get('jenis_pengembalian', record.jenis_pengembalian),
                'percent_pembulatan': vals.get('percent_pembulatan', record.percent_pembulatan),
                'disonfaktur': vals.get('disonfaktur', record.disonfaktur),
                'faktur_eklusif': vals.get('faktur_eklusif', record.faktur_eklusif),
                'eklusif_awal': formatted_eklusif_awal,
                'eklusif_akhir': formatted_eklusif_akhir,
                'nama_bm': vals.get('nama_bm', record.nama_bm),
                'id_karyawan': vals.get('id_karyawan', record.id_karyawan),
                'time_stamp': formatted_time_stamp,
                'harga_acuan': vals.get('harga_acuan', record.harga_acuan),
                'nomor_nppkp': vals.get('nomor_nppkp', record.nomor_nppkp),
                'tgl_pkp': formatted_tgl_pkp,
                'mata_uang': vals.get('mata_uang', record.mata_uang),
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)

            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/Prinsipal/updatePrinsipal",
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
        return super(prinsipal, self).unlink()
    
    def delete_from_external_api(self, record):
        data_to_send = {
            'kode_principal': record.kode_principal
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.delete(
                "http://192.168.16.130/microservice_internal/produk/Prinsipal/deletePrinsipal",
                json=data_to_send,
                headers=headers
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Gagal menghapus data dari API eksternal: %s", e)
            raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

        _logger.info("Sukses: Data dihapus dari API eksternal.")

        