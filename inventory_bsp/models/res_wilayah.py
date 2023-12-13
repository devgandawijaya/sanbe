from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)

class wilayahProvinsi(models.Model):

    _name = 'wilayah.provinsi'
    _rec_name = 'nama_provinsi'

    kode_provinsi = fields.Char()
    id_negara = fields.Char()
    nama_negara = fields.Char()
    nama_provinsi = fields.Char()

class WilayahKota(models.Model):
    _name = 'wilayah.kota'
    _rec_name = 'nama_kabupaten_kota'


    kode_kabkot = fields.Char(string='Kode Kabupaten/Kota')
    kode_provinsi_id = fields.Many2one('wilayah.provinsi', string='Provinsi')
    nama_kabupaten_kota = fields.Char(string='Nama Kabupaten/Kota')
    

class WilayahKecamatan(models.Model):
    _name = 'wilayah.kecamatan'
    _rec_name = 'nama_kecamatan'


    id_kecamatan = fields.Char(string='ID Kecamatan', required=True)
    kode_kabkot_id = fields.Many2one('wilayah.kota', string='Kota/Kabupaten', required=True)
    nama_kecamatan = fields.Char(string='Nama Kecamatan', required=True)


class WilayahKelurahan(models.Model):
    _name = 'wilayah.kelurahan'
    _rec_name = 'nama_kelurahan'


    id_kelurahan = fields.Char(string='ID Kelurahan', required=True)
    id_kecamatan_id = fields.Many2one('wilayah.kecamatan', string='Kecamatan', required=True)
    nama_kelurahan = fields.Char(string='Nama Kelurahan', required=True)
    kode_pos = fields.Char(string='Kode Pos')

