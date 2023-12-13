from odoo import models, fields


class MasterGudang(models.Model):
    _inherit = 'stock.warehouse'

    code = fields.Char(size=20)
    alamat_gudang = fields.Char()
    jumlah_freezer = fields.Char()
    kode_kabupaten_kota_id = fields.Many2one('wilayah.kota', string='Nama Kota/Kabupaten')
    keterangan_gudang = fields.Char()
    jenis_gudang = fields.Char()
    kategori_gudang = fields.Char()
    karyawan_id = fields.Many2one(
        'hr.employee', 
        string='Nama Karyawan', 
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    )
    kode_cabang_id = fields.Many2one('res.company', string='Kode Cabang',context={'show_kode_cabang': True})


    def name_get(self):
        if self.env.context.get('show_kode_gudang'):
            return [(record.id, record.code) for record in self]
        else:
            return [(record.id, record.name) for record in self]