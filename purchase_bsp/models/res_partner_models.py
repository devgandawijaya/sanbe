from odoo import models, fields, api

class ResPartnerInheritBSP(models.Model):
    _inherit = 'res.partner'

    kode_principal = fields.Char(string="Kode Prinsipal")
    cp_logistik = fields.Char(string='CP Logistic Prinsipal')
    cp_finance = fields.Char(string='CP Finance Prinsipal')
    cp_marketing = fields.Char(string='CP Marketing Prinsipal')
    fax_principal = fields.Char(string='No Fax')
    npwp_principal = fields.Char(string='No NPWP')
    tanggal_bergabung = fields.Date(string='Tanggal Bergabung')
    tanggal_berhenti = fields.Date(string='Tanggal Berhenti')
    percent_pembulat = fields.Integer(string='Persen Pembulatan')
    jenis_pengembalian = fields.Char(string='Jenis Pengembalian')
    diskon_faktur = fields.Char(string='Diskon Faktur')
    faktur_ekslusif = fields.Char(string='Faktur Ekslusif')
    ekslusif_awal = fields.Char(string='Ekslusif Awal')
    ekslusif_akhir = fields.Char(string='Ekslusif Akhir')
    nama_bm = fields.Char(string='Nama BM')
    harga_acuan = fields.Char(string='Harga Acuan')
    nomor_nppkp = fields.Char(string='Nomor NPPKP')
    tgl_pkp = fields.Date(string='Tanggal PKP')
    is_bsp_prinsipal = fields.Boolean('Is BSP Prinsipal', default=False)