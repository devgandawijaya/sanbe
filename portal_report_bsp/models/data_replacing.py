from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import logging
from ..controllers.constants import CABANG as list_cabang

_logger = logging.getLogger(__name__)

class dataReplacingScchoosedivorbrg(models.Model):
    _name = 'data.replacing.choosedivorbrg'

    name = fields.Char()

class dataReplacing(models.Model):
    _name = 'data.replacing'

    vcabang = fields.Char()
    vNamaCabang_id  = fields.Many2one('res.company',string='Nama Cabang')
    vawal = fields.Date(string='Tanggal Awal')
    vakhir = fields.Date(string='Tanggal Akhir')
    speriodeawal = fields.Char(string='Periode Awal', compute='_compute_speriodeawal', store=True)      
    speriodeakhir = fields.Char(string='Periode Akhir', compute='_compute_speriodeakhir', store=True)  
    sdivproduk = fields.Selection([('Divisi', 'Divisi'), ('Item', 'Item')])
    schoosedivorbrg_ids = fields.Many2many('product.divisi', string='Schoose')
    # schoosedivorbrg_ids = fields.Many2many('product.divisi' , string='Schoose')
    sbonus = fields.Selection([('YA', 'YA'),('TIDAK', 'TIDAK')])    
    sTabSufffix = fields.Char(default='192_168_5_2023')

    kode_cabang = fields.Char('Kode Cabang')
    nama_cabang_id = fields.Char(string='Nama Cabang Master')
    kode_barang_id = fields.Char(string='Kode Barang')
    nama_barang = fields.Char('Nama Barang')
    kode_divisi_produk_id = fields.Char(string='Kode Produk Divisi')
    partner_id = fields.Char(string='Nama Vendor')
    kode_principal = fields.Char(string='Kode Vendor')
    kode_barang_principal = fields.Char()
    ssl_cbg_levelasal = fields.Char()
    ssl_cbg_levelkecil = fields.Char()
    harga_beli_terkecil = fields.Char()
    stock_avail = fields.Char()
    stock_avail_rp = fields.Char()
    pending = fields.Char()
    pending_rp = fields.Char()
    intransit = fields.Char()
    intransit_rp = fields.Char()
    orderr = fields.Char()
    order_rp = fields.Char()
    ratio = fields.Char()
    sales = fields.Char()
    sales_rp = fields.Char()
    faktor_pengali = fields.Char()
    ssl_fix = fields.Char()
    ket_divisi = fields.Char()
    flag_ratio = fields.Char()
    tgl_berlaku_ssl = fields.Date()
    stock_good = fields.Char()
    fetch_date = fields.Date()
    startdate = fields.Date(string='Start Date')
    enddate = fields.Date(string='End Date')
    delete_after_process = fields.Boolean(default=False)
    rb_index = fields.Char()

    @api.onchange('vNamaCabang_id')
    def _onchange_vNamaCabang_id(self):
        if self.vNamaCabang_id:
            self.vcabang = self.vNamaCabang_id.kode_cabang
        else:
            self.vcabang = False

    @api.depends('vawal')
    def _compute_speriodeawal(self):
        for record in self:
            if record.vawal:
                record.speriodeawal = record.vawal.strftime('%Y%m')
            else:
                record.speriodeawal = False

    @api.depends('vakhir')
    def _compute_speriodeakhir(self):
        for record in self:
            if record.vakhir:
                record.speriodeakhir = record.vakhir.strftime('%Y%m')
            else:
                record.speriodeakhir = False

    def button_data_replacing(self):
        self.ensure_one()
        self.delete_after_process = True
        self.env.cr.commit()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "{}/call_stored_procedure".format(base_url)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }

    
    def action_export_pdf(self):
        return self.env.ref('portal_report_bsp.action_report_data_replacing_pdf').report_action(self)



    
    # Automated method for Get Data Replacing data 
    def cron_get_data_replacing_per_batch(self):
        # base_url = "http://192.168.16.130/portal/bis_{}/bisreport/getDataReplacing"
        base_url = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getReplacingBarang/?kode_cabang={}"
        

        for branch_name, abbreviation in list_cabang.items():
            current_ext_url = base_url.format(abbreviation.upper())

            print(f'Cronjob is currently requesting data for branch: {branch_name}, with abbreviation: {abbreviation}, URL: {current_ext_url}')   

            try:
                response = requests.get(current_ext_url)
                response.raise_for_status()

                if response.status_code != 200:
                    print(f"External Data Replacing endpoint for branch {branch_name} didn't respond with status 200")
                else:
                    print(f"Data Replacing data for branch {branch_name} successfully retrieved by cronjob")

            except requests.exceptions.RequestException as err:
                error_message = f"Error during GET request: {err}"
                print(error_message)
                _logger.error(error_message)