from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class cabangMaster(models.Model):
    _name = 'cabang.master'
    _rec_name = 'nama_cabang'

    kode_cabang = fields.Char()
    nama_cabang = fields.Char()
    tlp_cabang = fields.Char()
    fax_cabang = fields.Char()
    email_cabang = fields.Char()
    alamat_cabang = fields.Char()
    npwp_cabang = fields.Char()
    npwp_tanggal = fields.Char()
    sk_mentri = fields.Char()
    nomor_seri_pajak = fields.Char()
    no_izin = fields.Char()
    akhir_bulan_berlaku = fields.Char()
    penangung_jawab = fields.Char()
    sik_aa = fields.Char()
    tanggal_berdiri = fields.Char()
    kode_provinsi_id = fields.Many2one('wilayah.provinsi', string='Nama Provinsi')
    nik_kepala_cabang = fields.Char()
    no_izin_akses = fields.Char()
    penanggung_jawab_alkes = fields.Char()
    sik_aa_alkes = fields.Char()
    kagud = fields.Char()
    karyawan_id = fields.Many2one(
        'hr.employee', 
        string='Nama Karyawan', 
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    )
    kode_negara = fields.Char(related='kode_provinsi_id.nama_negara', string='Nama Negara', readonly=True, store=True)

    def name_get(self):
        if self.env.context.get('show_kode_cabang'):
            return [(record.id, record.kode_cabang) for record in self]
        else:
            return [(record.id, record.nama_cabang) for record in self]
    # Post data
    @api.model
    def create(self, vals):
        _logger.debug("Creating cabang.master with vals: %s", vals)
        # record = self.env['product.categories'].create(vals)
        record = super(cabangMaster, self).create(vals)
        self.post_to_external_api(record)
        return record

    def post_to_external_api(self, record):
        data_to_send = {
            'kode_cabang': record.kode_cabang,
            'nama_cabang': record.nama_cabang,
            'tlp_cabang': record.tlp_cabang,
            'fax_cabang': record.fax_cabang,
            'email_cabang': record.email_cabang,
            'alamat_cabang': record.alamat_cabang,
            'npwp_cabang': record.npwp_cabang,
            'npwp_tanggal': record.npwp_tanggal,
            'sk_mentri': record.sk_mentri,
            'nomor_seri_pajak': record.nomor_seri_pajak,
            'no_izin': record.no_izin,
            'akhir_bulan_berlaku': record.akhir_bulan_berlaku,
            'penangung_jawab': record.penangung_jawab,
            'sik_aa': record.sik_aa,
            'tanggal_berdiri': record.tanggal_berdiri,
            'kode_provinsi': record.kode_provinsi_id.nama_provinsi if record.kode_provinsi_id else None,
            'nik_kepala_cabang': record.nik_kepala_cabang,
            'no_izin_akses': record.no_izin_akses,
            'penanggung_jawab_alkes': record.penanggung_jawab_alkes,
            'sik_aa_alkes': record.sik_aa_alkes,
            'kagud': record.kagud,
            'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
            'kode_negara': record.kode_negara
        }
        _logger.info("Data to send to external API: %s", data_to_send)

        try:
            response = requests.post(
                "http://192.168.16.130/microservice_internal/produk/Prinsipal/addCabang",
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
        result = super(cabangMaster, self).write(vals)
        if result:
            self.update_to_external_api(vals)
        return result

    def update_to_external_api(self, vals):
        for record in self:
            data_to_send = {
                'kode_cabang': record.kode_cabang,
                'nama_cabang': record.nama_cabang,
                'tlp_cabang': record.tlp_cabang,
                'fax_cabang': record.fax_cabang,
                'email_cabang': record.email_cabang,
                'alamat_cabang': record.alamat_cabang,
                'npwp_cabang': record.npwp_cabang,
                'npwp_tanggal': record.npwp_tanggal,
                'sk_mentri': record.sk_mentri,
                'nomor_seri_pajak': record.nomor_seri_pajak,
                'no_izin': record.no_izin,
                'akhir_bulan_berlaku': record.akhir_bulan_berlaku,
                'penangung_jawab': record.penangung_jawab,
                'sik_aa': record.sik_aa,
                'sik_aa_alkes': record.sik_aa_alkes,
                'penanggung_jawab_alkes': record.penanggung_jawab_alkes,
                'kode_provinsi': record.kode_provinsi_id.nama_provinsi if record.kode_provinsi_id else None,
                'nik_kepala_cabang': record.nik_kepala_cabang,
                'no_izin_akses': record.no_izin_akses,
                'kagud': record.kagud,
                'id_karyawan': record.karyawan_id.name if record.karyawan_id else None,
                'tanggal_berdiri': record.tanggal_berdiri,
            }
            _logger.info("Data to send for update to external API: %s", data_to_send)

            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.put(
                    "http://192.168.16.130/microservice_internal/produk/Prinsipal/updateCabang",
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
        return super(cabangMaster, self).unlink()
    
    def delete_from_external_api(self, record):
        data_to_send = {
            'kode_cabang': record.kode_cabang
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.delete(
                "http://192.168.16.130/microservice_internal/produk/Prinsipal/deleteCabang/",
                json=data_to_send,
                headers=headers
            )
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            _logger.error("Gagal menghapus data dari API eksternal: %s", e)
            raise UserError('Gagal menghapus data dari API eksternal: {}'.format(e))

        _logger.info("Sukses: Data dihapus dari API eksternal.")