from odoo import models, fields, api
import json
import requests
import logging
from ..controllers.constants import CABANG as list_cabang

logging.basicConfig(filename='cron_log.txt', level=logging.ERROR)
_logger = logging.getLogger(__name__)

class BarangDatangSChooseDivorBrg(models.Model):
    _name = 'barang.datang.schoosedivorbrg'

    name = fields.Char()

class BarangDatangModel(models.Model):
    _name = 'barang.datang'

    # These fields are only for user input
    # v_kode_cabang = fields.Char(string='Cabang')
    # v_nama_cabang_id = fields.Many2one('cabang.master',string='Nama Cabang')  
    # v_date_awal = fields.Date(string='Tanggal Awal')
    # v_date_akhir = fields.Date(string='Tanggal Akhir')
    # s_tab_suffix = fields.Char(string='Tabel Suffix', default='192_168_5_2023')
    # s_choosedivorbrg_ids = fields.Many2many('barang.datang.schoosedivorbrg', string='Schoose')
    # s_bonus = fields.Selection([('YA', 'YA'),('TIDAK', 'TIDAK')], default='YA')    
    # s_div_produk = fields.Selection([('Divisi', 'Divisi'), ('Item', 'Item')], default='Divisi')
    # s_total = fields.Char(string='Total Data', default='ALL')

    # These fields are only for user treeview display
    kode_cabang = fields.Char(related='nama_cabang_id.kode_cabang',string='Branch Code', readonly=True)
    nama_cabang_id = fields.Many2one('res.company',string='Branch Name')
    no_barang_datang = fields.Char(string='Incoming Goods Number')
    tgl_bd = fields.Char('Date BD')
    tgl_po = fields.Char('Date PO')
    no_surat_jalan = fields.Char(string='Delivery Note Number')
    no_bpb = fields.Char(string='BPB Number')
    no_spb = fields.Char(string='SPB Number')
    no_do = fields.Char(string='DO Number')
    no_po = fields.Char(string='PO Number')
    tglpajak = fields.Char(string='Tax Date')
    nopajak = fields.Char(string='Tax Number')
    topfkt = fields.Char(string='TOP FKT')
    jenis_faktur = fields.Char('Invoice Type')
    jenis_beli = fields.Char('Buy Type')
    jenis_mac = fields.Char('Mac Type')    
    sub_jenis_beli = fields.Char(string='Sub Purchase Type')
    pcpl_kode = fields.Char(string='PCPL Code')
    noitem = fields.Integer(string='Item Number')
    kode_barang_id = fields.Many2one('product.template', string='Kode Barang', context={'show_kode_barang': True})
    kode_barang_bis = fields.Char(string='Alternative Product Code')
    nama_barang = fields.Char(related='kode_barang_id.name', readonly=True)
    nobatch = fields.Char(string='Batch Number')
    qty_transaksi = fields.Char(string='Transaction Quantity')
    satuan_transaksi = fields.Char(string='Transaction Unit')
    harga_transaksi = fields.Char(string='Transaction Price')
    qty_beli_terkecil = fields.Char(string='Smallest Purchase Quantity')
    harga_beli_terkecil = fields.Char(string='Smallest Purchase Price')
    satuan_beli_terkecil = fields.Char(string='Smallest Purchase Unit')
    ssl_pr = fields.Char(string='SSL PR')
    qty_order_terkecil = fields.Char(string='Smallest Order Quantity')
    satuan_order_terkecil = fields.Char(string='Smallest Order Unit')
    harga_order_terkecil = fields.Char(string='Smallest Order Price')
    qty_besar = fields.Char(string='Largest Quantity')
    harga_beli_terbesar = fields.Char(string='Largest Purchase Price')
    satuan_beli_terbesar = fields.Char(string='Largest Purchase Unit')
    tgl_ed = fields.Char(string='Expiration Date')
    bonus = fields.Char(string='Bonus')
    gross = fields.Char(string='Gross Amount')
    netto = fields.Char(string='Net Amount')
    kode_divisi_produk_id = fields.Many2one('product.divisi',string='Kode Produk Divisi')
    partner_id = fields.Many2one('res.partner', string='Nama Vendor')
    kode_principal = fields.Char(related='partner_id.name', string='Kode Vendor', readonly=True)
    status_terkirim = fields.Char('Delivery Status')
    status_barang = fields.Char('Product Status')
    flagdepo = fields.Char(string='Depo Flag')
    kurir = fields.Char(string='Courier')
    status_quo_barang = fields.Char('Product Status Quo')
    catatan = fields.Text(string='Note')
    dosub = fields.Char(string='Do Sub')
    bulando = fields.Char(string='Bulan DO')
    cbgitem = fields.Char(string='Item Branch')
    tanggal_penarikan_awal = fields.Date('Tanggal Penarikan Awal')
    tanggal_penarikan_akhir = fields.Date('Tanggal Penarikan Akhir')
    fetch_date = fields.Date()
    bd_index = fields.Integer('BD Index')

    # This field is only used for flagging another fields
    is_input = fields.Boolean(string='Is Input', default=False)

    # @api.onchange('v_nama_cabang_id')
    # def _onchange_v_nama_cabang_id(self):
    #     if self.v_nama_cabang_id:
    #         self.v_kode_cabang = self.v_nama_cabang_id.kode_cabang
    #     else:
    #         self.v_kode_cabang = False

    def button_call_sp_barang_datang(self):
        self.ensure_one()
        self.is_input = True
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = f"{base_url}/spcall-barang-datang"
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }

    # Automated method for Get Barang Datang data 
    def cron_get_barang_datang_per_batch(self):
        # base_url = "http://192.168.16.130/portal/bis_{}/bisreport/getBarangDatang"
        # base_url = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getBarangDatang?kode_cabang={}"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = f"{base_url}/import-barang-datang"
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }
        # for branch_name, abbreviation in list_cabang.items():
        #     current_ext_url = base_url.format(abbreviation.upper())

        #     print(f'Cronjob is currently requesting data for branch: {branch_name}, with abbreviation: {abbreviation}, URL: {current_ext_url}')   

        #     try:
        #         response = requests.get(current_ext_url)
        #         response.raise_for_status()

        #         if response.status_code != 200:
        #             print(f"External Barang Datang endpoint for branch {branch_name} didn't respond with status 200")
        #         else:
        #             print(f"Barang Datang data for branch {branch_name} successfully retrieved by cronjob")

        #     except requests.exceptions.RequestException as err:
        #         error_message = f"Error during GET request: {err}"
        #         print(error_message)
        #         _logger.error(error_message)
