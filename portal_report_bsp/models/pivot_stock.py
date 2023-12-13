from odoo import models, fields, api

class PivotStock(models.Model):
    _name = 'pivot.stock'
    
    tgl_stock = fields.Date(string='Tanggal Stock')
    kode_cabang = fields.Char(string='Kode Cabang')
    kode_principal = fields.Char(string='Kode Prinsipal')
    Kode_Divisi_Produk_id = fields.Char(string='Kode Produk Divisi')
    kode_barang = fields.Char(string='Kode Barang')
    nama_barang_id = fields.Char(string='Nama Barang')
    rev_ssl = fields.Integer(string='SSL')
    avail_akhir = fields.Integer(string='Stock')
    ratio = fields.Char(string='Ratio', compute='_compute_ratio')

    @api.depends('rev_ssl', 'avail_akhir')
    def _compute_ratio(self):
        for record in self:
            if record.avail_akhir != 0:
                record.ratio = str(record.rev_ssl / record.avail_akhir)
            else:
                record.ratio = '0'
                
    def action_export_excel_pivot_stock(self):
        ids = ','.join(map(str, self.ids)) 
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "{}/pivot_stock/export_excel?ids={}".format(base_url, ids)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self'
        }