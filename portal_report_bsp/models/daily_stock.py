from odoo import models, fields, api
import json
import requests
import logging
from ..controllers.constants import CABANG as list_cabang

logging.basicConfig(filename='cron_log.txt', level=logging.ERROR)
_logger = logging.getLogger(__name__)

class DailyStockSChooseDivorBrg(models.Model):
    _name = 'daily.stock.schoosedivorbrg'

    name = fields.Char()

class DailyStockSChooseProsesstock(models.Model):
    _name = 'daily.stock.schooseprosesstock'

    name = fields.Char()

class DailyStock(models.Model):
    _name = 'daily.stock'

    # These fields are only for user input
    # s_kode_cabang = fields.Char(string='Cabang')
    # s_nama_cabang_id = fields.Many2one('cabang.master', string='Nama Cabang')
    # s_date_awal = fields.Date(string='Tanggal Awal')
    # s_date_akhir = fields.Date(string='Tanggal Akhir')
    # s_periode_awal = fields.Char(string='Periode Awal', compute='_compute_speriodeawal', store=True)      
    # s_periode_akhir = fields.Char(string='Perriode Akhir', compute='_compute_speriodeakhir', store=True)  
    # s_tab_suffix = fields.Char(string='Tabel Suffix', default='192_168_5_2023')
    # s_div_produk = fields.Selection([('Divisi', 'Divisi'), ('Item', 'Item')], default='Divisi')
    # s_bonus = fields.Selection([('YA', 'YA'),('TIDAK', 'TIDAK')], default='YA')    
    # s_choosedivorbrg_ids = fields.Many2many('daily.stock.schoosedivorbrg', string='Schoosedivorbrg')
    # s_chooseprosesstock_ids = fields.Many2many('daily.stock.schooseprosesstock', string='Schooseprosesstock')

    # These fields are only for user treeview display
    # kode_cabang = fields.Char(string='Branch Code')
    # nama_cabang = fields.Char(string='Branch Name')
    # kode_barang_clipper = fields.Char(string='Clipper Product Code')
    # kode_barang_bis = fields.Char(string='BIS Product Code')
    # kode_barang_principal = fields.Char(string='Principal Product Code')
    # group_barang = fields.Char(string='Product Group')
    # subgroup_barang = fields.Char(string='Product Subgroup')
    # sub_prc = fields.Char(string='Sub PRC')
    # category = fields.Char(string='Category')
    # unb_brand = fields.Char(string='UNB Brand')
    # type_barang = fields.Char(string='Product Type')
    # nama_barang = fields.Char(string='Product Name')
    # pcpl_kode_clipper = fields.Char(string='Clipper PCPL Code')
    # kode_principal = fields.Char(string='Principal Code')
    # Kode_Divisi_Produk = fields.Char(string='Product Division Code')
    # klasifikasi_jual = fields.Char(string='Selling Classification')
    # tgl_discontinue_pembelian = fields.Char(string='Buying Discontinue Date')
    # jenis_barang = fields.Char(string='Product Variant')
    # harga_jual_current = fields.Char(string='Current Sale Price')
    # harga_terkecil = fields.Char(string='Minimum Price')
    # harga_terbesar = fields.Char(string='Maximum Price')
    # qty1 = fields.Char(string='Qty 1')
    # satuan1 = fields.Char(string='Satuan 1')
    # qty2 = fields.Char(string='Qty 2')
    # satuan2 = fields.Char(string='Satuan 2')
    # qty3 = fields.Char(string='Qty 3')
    # satuan3 = fields.Char(string='Satuan 3')
    # qty4 = fields.Char(string='Qty 4')
    # satuan4 = fields.Char(string='Satuan 4')
    # avail_awal = fields.Char(string='Avail Awal')
    # avail_rp_awal = fields.Char(string='Avail RP Awal')
    # avail_q1_awal = fields.Char(string='Avail Q1 Awal')
    # avail_q2_awal = fields.Char(string='Avail Q2 Awal')
    # avail_q3_awal = fields.Char(string='Avail Q3 Awal')
    # avail_q4_awal = fields.Char(string='Avail Q4 Awal')
    # bs_awal = fields.Char(string='BS Awal')
    # bs_rp_awal = fields.Char(string='BS RP Awal')
    # bs_q1_awal = fields.Char(string='BS Q1 Awal')
    # bs_q2_awal = fields.Char(string='BS Q2 Awal')
    # bs_q3_awal = fields.Char(string='BS Q3 Awal')
    # bs_q4_awal = fields.Char(string='BS Q4 Awal')
    # dps_awal = fields.Char(string='DPS Awal')
    # dps_rp_awal = fields.Char(string='DPS RP Awal')
    # dps_q1_awal = fields.Char(string='DPS Q1 Awal')
    # dps_q2_awal = fields.Char(string='DPS Q2 Awal')
    # dps_q3_awal = fields.Char(string='DPS Q3 Awal')
    # dps_q4_awal = fields.Char(string='DPS Q4 Awal')
    # depo_awal = fields.Char(string='Depo Awal')
    # depo_rp_awal = fields.Char(string='Depo RP Awal')
    # depo_q1_awal = fields.Char(string='Depo Q1 Awal')
    # depo_q2_awal = fields.Char(string='Depo Q2 Awal')
    # depo_q3_awal = fields.Char(string='Depo Q3 Awal')
    # depo_q4_awal = fields.Char(string='Depo Q4 Awal')
    # bs_In = fields.Char(string='BS In')
    # bs_In_rp = fields.Char(string='BS In RP')
    # bs_In_q1 = fields.Char(string='BS In Q1')
    # bs_In_q2 = fields.Char(string='BS In Q2')
    # bs_In_q3 = fields.Char(string='BS In Q3')
    # bs_In_q4 = fields.Char(string='BS In Q4')
    # bs_out = fields.Char(string='BS Out')
    # bs_Out_rp = fields.Char(string='BS Out RP')
    # bs_Out_q1 = fields.Char(string='BS Out Q1')
    # bs_Out_q2 = fields.Char(string='BS Out Q2')
    # bs_Out_q3 = fields.Char(string='BS Out Q3')
    # bs_Out_q4 = fields.Char(string='BS Out Q4')
    # bs_adj = fields.Char(string='BS Adj')
    # bs_adj_rp = fields.Char(string='BS Adj RP')
    # bs_adj_q1 = fields.Char(string='BS Adj Q1')
    # bs_adj_q2 = fields.Char(string='BS Adj Q2')
    # bs_adj_q3 = fields.Char(string='BS Adj Q3')
    # bs_adj_q4 = fields.Char(string='BS Adj Q4')
    # dps_in = fields.Char(string='DPS In')
    # dps_In_rp = fields.Char(string='DPS In RP')
    # dps_In_q1 = fields.Char(string='DPS In Q1')
    # dps_In_q2 = fields.Char(string='DPS In Q2')
    # dps_In_q3 = fields.Char(string='DPS In Q3')
    # dps_In_q4 = fields.Char(string='DPS In Q4')
    # dps_Out = fields.Char(string='DPS Out')
    # dps_Out_rp = fields.Char(string='DPS Out RP')
    # dps_Out_q1 = fields.Char(string='DPS Out Q1')
    # dps_Out_q2 = fields.Char(string='DPS Out Q2')
    # dps_Out_q3 = fields.Char(string='DPS Out Q3')
    # dps_Out_q4 = fields.Char(string='DPS Out Q4')
    # dps_rtr = fields.Char(string='DPS RTR')
    # dps_rtr_rp = fields.Char(string='DPS RTR RP')
    # dps_rtr_q1 = fields.Char(string='DPS RTR Q1')
    # dps_rtr_q2 = fields.Char(string='DPS RTR Q2')
    # dps_rtr_q3 = fields.Char(string='DPS RTR Q3')
    # dps_rtr_q4 = fields.Char(string='DPS RTR Q4')
    # depo_In = fields.Char(string='Depo In')
    # depo_In_rp = fields.Char(string='Depo In RP')
    # depo_In_q1 = fields.Char(string='Depo In Q1')
    # depo_In_q2 = fields.Char(string='Depo In Q2')
    # depo_In_q3 = fields.Char(string='Depo In Q3')
    # depo_In_q4 = fields.Char(string='Depo In Q4')
    # depo_Out = fields.Char(string='Depo Out')
    # depo_Out_rp = fields.Char(string='Depo Out RP')
    # depo_Out_q1 = fields.Char(string='Depo Out Q1')
    # depo_Out_q2 = fields.Char(string='Depo Out Q2')
    # depo_Out_q3 = fields.Char(string='Depo Out Q3')
    # depo_Out_q4 = fields.Char(string='Depo Out Q4')
    # depo_rtr = fields.Char(string='Depo RTR')
    # depo_rtr_rp = fields.Char(string='Depo RTR RP')
    # depo_rtr_q1 = fields.Char(string='Depo RTR Q1')
    # depo_rtr_q2 = fields.Char(string='Depo RTR Q2')
    # depo_rtr_q3 = fields.Char(string='Depo RTR Q3')
    # depo_rtr_q4 = fields.Char(string='Depo RTR Q4')
    # beli = fields.Char(string='Beli')
    # rp_beli = fields.Char(string='RP Beli')
    # beli_q1 = fields.Char(string='Beli Q1')
    # beli_q2 = fields.Char(string='Beli Q2')
    # beli_q3 = fields.Char(string='Beli Q3')
    # beli_q4 = fields.Char(string='Beli Q4')
    # rtr_beli = fields.Char(string='RTR Beli')
    # rp_rtr_beli = fields.Char(string='RP RTR Beli')
    # rtr_beli_q1 = fields.Char(string='RTR Beli Q1')
    # rtr_beli_q2 = fields.Char(string='RTR Beli Q2')
    # rtr_beli_q3 = fields.Char(string='RTR Beli Q3')
    # rtr_beli_q4 = fields.Char(string='RTR Beli Q4')
    # jual = fields.Char(string='Jual')
    # rp_jual = fields.Char(string='RP Jual')
    # jual_q1 = fields.Char(string='Jual Q1')
    # jual_q2 = fields.Char(string='Jual Q2')
    # jual_q3 = fields.Char(string='Jual Q3')
    # jual_q4 = fields.Char(string='Jual Q4')
    # rtr_jual = fields.Char(string='RTR Jual')
    # rp_rtr_jual = fields.Char(string='RP RTR Jual')
    # rtr_jual_q1 = fields.Char(string='RTR Jual Q1')
    # rtr_jual_q2 = fields.Char(string='RTR Jual Q2')
    # rtr_jual_q3 = fields.Char(string='RTR Jual Q3')
    # rtr_jual_q4 = fields.Char(string='RTR Jual Q4')
    # mac_masuk = fields.Char(string='MAC Masuk')
    # rp_mac_masuk = fields.Char(string='RP MAC Masuk')
    # macIn_q1 = fields.Char(string='MAC In Q1')
    # macIn_q2 = fields.Char(string='MAC In Q2')
    # macIn_q3 = fields.Char(string='MAC In Q3')
    # macIn_q4 = fields.Char(string='MAC In Q4')
    # mac_keluar = fields.Char(string='MAC Keluar')
    # rp_mac_keluar = fields.Char(string='RP MAC Keluar')
    # macOut_q1 = fields.Char(string='MAC Out Q1')
    # macOut_q2 = fields.Char(string='MAC Out Q2')
    # macOut_q3 = fields.Char(string='MAC Out Q3')
    # macOut_q4 = fields.Char(string='MAC Out Q4')
    # adjust = fields.Char(string='Adjust')
    # rp_adjust = fields.Char(string='RP Adjust')
    # adj_q1 = fields.Char(string='Adjust Q1')
    # adj_q2 = fields.Char(string='Adjust Q2')
    # adj_q3 = fields.Char(string='Adjust Q3')
    # adj_q4 = fields.Char(string='Adjust Q4')
    # avail_akhir = fields.Char(string='Avail Akhir')
    # avail_rp_akhir = fields.Char(string='Avail RP Akhir')
    # avail_q1_akhir = fields.Char(string='Avail Q1 Akhir')
    # avail_q2_akhir = fields.Char(string='Avail Q2 Akhir')
    # avail_q3_akhir = fields.Char(string='Avail Q3 Akhir')
    # avail_q4_akhir = fields.Char(string='Avail Q4 Akhir')
    # bs_akhir = fields.Char(string='BS Akhir')
    # bs_rp_akhir = fields.Char(string='BS RP Akhir')
    # bs_q1_akhir = fields.Char(string='BS Q1 Akhir')
    # bs_q2_akhir = fields.Char(string='BS Q2 Akhir')
    # bs_q3_akhir = fields.Char(string='BS Q3 Akhir')
    # bs_q4_akhir = fields.Char(string='BS Q4 Akhir')
    # dps_akhir = fields.Char(string='DPS Akhir')
    # dps_rp_akhir = fields.Char(string='DPS RP Akhir')
    # dps_q1_akhir = fields.Char(string='DPS Q1 Akhir')
    # dps_q2_akhir = fields.Char(string='DPS Q2 Akhir')
    # dps_q3_akhir = fields.Char(string='DPS Q3 Akhir')
    # dps_q4_akhir = fields.Char(string='DPS Q4 Akhir')
    # depo_akhir = fields.Char(string='Depo Akhir')
    # depo_rp_akhir = fields.Char(string='Depo RP Akhir')
    # depo_q1_akhir = fields.Char(string='Depo Q1 Akhir')
    # depo_q2_akhir = fields.Char(string='Depo Q2 Akhir')
    # depo_q3_akhir = fields.Char(string='Depo Q3 Akhir')
    # depo_q4_akhir = fields.Char(string='Depo Q4 Akhir')
    # ag_akhir = fields.Char(string='AG Akhir')
    # ag_rp_akhir = fields.Char(string='AG RP Akhir')
    # ag_q1_akhir = fields.Char(string='AG Q1 Akhir')
    # ag_q2_akhir = fields.Char(string='AG Q2 Akhir')
    # ag_q3_akhir = fields.Char(string='AG Q3 Akhir')
    # ag_q4_akhir = fields.Char(string='AG Q4 Akhir')
    # no_batch = fields.Char(string='No Batch')
    # tgl_expired = fields.Char(string='Tanggal Expired')
    # bs_akhir_reject = fields.Char(string='BS Akhir Reject')
    # bs_rp_akhir_reject = fields.Char(string='BS RP Akhir Reject')
    # bs_q1_akhir_reject = fields.Char(string='BS Q1 Akhir Reject')
    # bs_q2_akhir_reject = fields.Char(string='BS Q2 Akhir Reject')
    # bs_q3_akhir_reject = fields.Char(string='BS Q3 Akhir Reject')
    # bs_q4_akhir_reject = fields.Char(string='BS Q4 Akhir Reject')
    # bs_akhir_defect = fields.Char(string='BS Akhir Defect')
    # bs_rp_akhir_defect = fields.Char(string='BS RP Akhir Defect')
    # bs_q1_akhir_defect = fields.Char(string='BS Q1 Akhir Defect')
    # bs_q2_akhir_defect = fields.Char(string='BS Q2 Akhir Defect')
    # bs_q3_akhir_defect = fields.Char(string='BS Q3 Akhir Defect')
    # bs_q4_akhir_defect = fields.Char(string='BS Q4 Akhir Defect')
    # bs_akhir_pending = fields.Char(string='BS Akhir Pending')
    # bs_rp_akhir_pending = fields.Char(string='BS RP Akhir Pending')
    # bs_q1_akhir_pending = fields.Char(string='BS Q1 Akhir Pending')
    # bs_q2_akhir_pending = fields.Char(string='BS Q2 Akhir Pending')
    # bs_q3_akhir_pending = fields.Char(string='BS Q3 Akhir Pending')
    # bs_q4_akhir_pending = fields.Char(string='BS Q4 Akhir Pending')
    # bs_akhir_hold = fields.Char(string='BS Akhir Hold')
    # bs_rp_akhir_hold = fields.Char(string='BS RP Akhir Hold')
    # bs_q1_akhir_hold = fields.Char(string='BS Q1 Akhir Hold')
    # bs_q2_akhir_hold = fields.Char(string='BS Q2 Akhir Hold')
    # bs_q3_akhir_hold = fields.Char(string='BS Q3 Akhir Hold')
    # bs_q4_akhir_hold = fields.Char(string='BS Q4 Akhir Hold')
    # keluar_tender = fields.Char(string='Keluar Tender')
    # keluar_tender_rp = fields.Char(string='Keluar Tender RP')
    # keluar_tender_q1 = fields.Char(string='Keluar Tender Q1')
    # keluar_tender_q2 = fields.Char(string='Keluar Tender Q2')
    # keluar_tender_q3 = fields.Char(string='Keluar Tender Q3')
    # keluar_tender_q4 = fields.Char(string='Keluar Tender Q4')
    # keluar_hc = fields.Char(string='Keluar HC')
    # keluar_hc_rp = fields.Char(string='Keluar HC RP')
    # keluar_hc_q1 = fields.Char(string='Keluar HC Q1')
    # keluar_hc_q2 = fields.Char(string='Keluar HC Q2')
    # keluar_hc_q3 = fields.Char(string='Keluar HC Q3')
    # keluar_hc_q4 = fields.Char(string='Keluar HC Q4')
    # bs_current_reject = fields.Char(string='BS Current Reject')
    # bs_current_defect = fields.Char(string='BS Current Defect')
    # bs_current_pending = fields.Char(string='BS Current Pending')
    # bs_current_hold = fields.Char(string='BS Current Hold')
    # tgl_stock = fields.Char(string='Tanggal Stock')
    # sslx = fields.Char(string='SSLX')
    # rev_ssl = fields.Char(string='Rev SSL')
    # sslx_kecil = fields.Char(string='SSLX Kecil')
    # rev_ssl_kecil = fields.Char(string='Rev SSL Kecil')
    # startdate = fields.Date()
    # enddate = fields.Date()
    # fetch_date = fields.Date()

    kode_cabang = fields.Char(string='kode Cabang')
    nama_cabang_id = fields.Char(string='Nama Cabang')
    kode_barang = fields.Char(string='Kode Barang')
    # kode_barang_clipper = fields.Char('Kode Clipper')
    kode_barang_principal = fields.Char('Kode Prinsipal Barang')
    group_barang = fields.Char('Grup')
    category_barang = fields.Char(string='Kategori')
    nama_barang_id = fields.Char(string='Nama Barang')
    partner_id = fields.Char(string='Nama Vendor')
    kode_principal = fields.Char(string='kode Vendor')
    Kode_Divisi_Produk_id = fields.Char()
    jenis_barang = fields.Char('Jenis')
    harga_terkini = fields.Char('Harga Terkini')
    harga_terkecil = fields.Char('Harga Terkecil')
    harga_terbesar = fields.Char('Harga Terbesar')
    qty_satuan = fields.Char('Jumlah Satuan')
    satuan_terbesar = fields.Char('Satuan Terbesar')
    qty_satuan_kecil = fields.Char('Jumlah Satuan Kecil')
    satuan_terkecil = fields.Char('Satuan Terkecil')
    qty_awal = fields.Char('Persediaan Awal')
    qty_akhir = fields.Char('Persediaan Akhir')
    tanggal_penarikan_awal = fields.Date('Tanggal Penarikan Awal')
    tanggal_penarikan_akhir = fields.Date('Tanggal Penarikan Akhir')
    tgl_stock = fields.Date(string='Tanggal Stock')
    rev_ssl = fields.Integer(string='Rev SSL')
    avail_akhir = fields.Integer(string='Avail Akhir')
    ds_index = fields.Integer('DS Index')
    fetch_date = fields.Date('Fetch Date')
    

    # This field is only used for flagging another fields
    is_input = fields.Boolean('Is Input')
    
    # @api.onchange('s_nama_cabang_id')
    # def _onchange_s_nama_cabang_id(self):
    #     if self.s_nama_cabang_id:
    #         self.s_kode_cabang = self.s_nama_cabang_id.kode_cabang
    #     else:
    #         self.s_kode_cabang = False

    # @api.depends('s_date_awal')
    # def _compute_speriodeawal(self):
    #     for record in self:
    #         if record.s_date_awal:
    #             record.s_periode_awal = record.s_date_awal.strftime('%Y%m')
    #         else:
    #             record.s_periode_awal = False

    # @api.depends('s_date_akhir')
    # def _compute_speriodeakhir(self):
    #     for record in self:
    #         if record.s_date_akhir:
    #             record.s_periode_akhir = record.s_date_akhir.strftime('%Y%m')
    #         else:
    #             record.s_periode_akhir = False

    def button_call_sp_daily_stock(self):
        self.ensure_one()
        self.is_input = True
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = f"{base_url}/import-daily-stock"
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }
    
    # Automated method for Get Daily Stock data 
    def cron_get_daily_stock_per_batch(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = f"{base_url}/import-daily-stock"
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }
        # base_url = "http://192.168.16.130/portal/bis_{}/bisreport/getDailyStock"
        # base_url = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getDailyStock?kode_cabang={}"

        # for branch_name, abbreviation in list_cabang.items():
        #     current_ext_url = base_url.format(abbreviation.upper())

        #     print(f'Cronjob is currently requesting data for branch: {branch_name}, with abbreviation: {abbreviation}, URL: {current_ext_url}')   

        #     try:
        #         response = requests.get(current_ext_url)
        #         response.raise_for_status()

        #         if response.status_code != 200:
        #             print(f"External Daily Stock endpoint for branch {branch_name} didn't respond with status 200")
        #         else:
        #             print(f"Daily Stock data for branch {branch_name} successfully retrieved by cronjob")

        #     except requests.exceptions.RequestException as err:
        #         error_message = f"Error during GET request: {err}"
        #         print(error_message)
        #         _logger.error(error_message)