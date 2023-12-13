from odoo import models, fields, api

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    cp_logistik = fields.Char(related="partner_id.cp_logistik", string='CP Logistic Prinsipal')
    cp_finance = fields.Char(related="partner_id.cp_finance", string='CP Finance Prinsipal')
    cp_marketing = fields.Char(related="partner_id.cp_marketing", string='CP Marketing Prinsipal')
    fax_principal = fields.Char(related="partner_id.fax_principal", string='Fax Prinsipal')
    npwp_principal = fields.Char(related="partner_id.npwp_principal", string='NPWP Prinsipal')
    tanggal_bergabung = fields.Date(related="partner_id.tanggal_bergabung", string='Tanggal Bergabung Prinsipal')
    tanggal_berhenti = fields.Date(related="partner_id.tanggal_berhenti", string='Tanggal Berhenti Prinsipal')
    percent_pembulat = fields.Integer(related="partner_id.percent_pembulat", string='Persen Pembulatan Prinsipal')
    jenis_pengembalian = fields.Char(related="partner_id.jenis_pengembalian", string='Jenis Pengembalian Prinsipal')
    diskon_faktur = fields.Char(related="partner_id.diskon_faktur", string='Diskon Faktur Prinsipal')
    faktur_ekslusif = fields.Char(related="partner_id.faktur_ekslusif", string='Faktur Ekslusif Prinsipal')
    ekslusif_awal = fields.Char(related="partner_id.ekslusif_awal", string='Ekslusif Awal Prinsipal')
    ekslusif_akhir = fields.Char(related="partner_id.ekslusif_akhir", string='Ekslusif Akhir Prinsipal')
    nama_bm = fields.Char(related="partner_id.nama_bm", string='Nama BM Prinsipal')
    harga_acuan = fields.Char(related="partner_id.harga_acuan", string='Harga Acuan Prinsipal')
    nomor_nppkp = fields.Char(related="partner_id.nomor_nppkp", string='Nomor NPPKP Prinsipal')
    tgl_pkp = fields.Date(related="partner_id.tgl_pkp", string='Tanggal PKP Prinsipal')