from odoo import models, fields, api


class transporterMaster(models.Model):
    _name = 'transporter.master'
    
    kode_transporter = fields.Char()
    nama_transporter = fields.Char()
    descripsi_transporter = fields.Text()    
    cabang_master_ids = fields.Many2many('res.company')