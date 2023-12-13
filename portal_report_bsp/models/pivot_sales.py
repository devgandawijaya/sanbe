from odoo import models, fields, api
import json
import requests
import logging

class PivotSalesModel(models.Model):
    _name = 'pivot.sales'
    
    konsolidasi_id = fields.Many2one('konsolidasi.master', string='Konsolidasi')
    kode_cabang = fields.Char(related='konsolidasi_id.kode_cabang_id', string='Kode Cabang')
    kode_barang = fields.Char(related='konsolidasi_id.kode_barang_id', string='Kode Barang')
    tgl_faktur = fields.Date(related='konsolidasi_id.tgl_faktur')
    jenis_faktur = fields.Char(related='konsolidasi_id.jenis_faktur')
    flag_barang = fields.Char(related='konsolidasi_id.flag_barang')
    status_barang = fields.Char(related='konsolidasi_id.status_barang')
    gross = fields.Float(related='konsolidasi_id.gross')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')