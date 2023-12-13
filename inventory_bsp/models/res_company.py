from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    tax_lock_date = fields.Datetime()
    kode_cabang = fields.Char(string='Kode Cabang')
    fax_cabang = fields.Char(string='FAX Cabang')
    sk_mentri = fields.Char(string='Surat Keterangan Mentri')
    nomor_seri_pajak = fields.Char(string='Nomor Seri Pajak')
    no_izin = fields.Char(string='NO. Izin')
    akhir_bulan_berlaku = fields.Datetime(string='Akhir Bulan Berlaku')
    penangung_jawab = fields.Char(string='Penanggung Jawab')
    sik_aa = fields.Char(string='SIK AA')
    tanggal_berdiri = fields.Datetime(string='Tanggal Berdiri')
    # kode_provinsi_id = fields.Many2one('wilayah.provinsi', string='Nama Provinsi')
    nik_kepala_cabang = fields.Char(string='NIK Kepala Cabang')
    no_izin_akses = fields.Char(string='No Izin Akses')
    penanggung_jawab_alkes = fields.Char(string='Penangung Jawab ALKES')
    sik_aa_alkes = fields.Char(string='SIK AA ALKES')
    kagud = fields.Char(string='KADUG')
    karyawan_id = fields.Many2one(
        'hr.employee', 
        string='Nama Karyawan', 
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    )
    # kode_negara = fields.Char(related='kode_provinsi_id.nama_negara', string='Nama Negara', readonly=True, store=True)
    
    def name_get(self):
        if self.env.context.get('show_kode_cabang'):
            return [(record.id, record.kode_cabang) for record in self]
        else:
            return [(record.id, record.name) for record in self]