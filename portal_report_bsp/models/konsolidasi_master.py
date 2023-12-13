from odoo import models, fields, api
import requests
from odoo.exceptions import UserError
import logging
from ..controllers.constants import CABANG as list_cabang

_logger = logging.getLogger(__name__)



class KonsolidasiMaster(models.Model):
    _name = 'konsolidasi.master'

    kode_cabang_id = fields.Char(string='Kode Cabang')
    kode_gudang_id = fields.Char(string='Kode Cabang')
    kode_barang_id = fields.Char(string='Kode Cabang')
    satuan_purchaselvl = fields.Char()
    satuan_Yjual_kecil = fields.Char()
    satuan_sp_terkecil = fields.Char()
    satuan_faktur_terkecil = fields.Char()
    satuan_sp = fields.Char()
    satuan_sales = fields.Char()
    flag_barang = fields.Char()
    sp_kode_jenis_jual = fields.Char()
    sp_banded = fields.Char()
    no_referensi_order = fields.Char()
    ponumber = fields.Char()
    pomtc = fields.Char()
    kode_salesman = fields.Char()
    flagsp = fields.Char()
    flagsales = fields.Char()
    via = fields.Char()
    status_sp = fields.Char()
    no_batch = fields.Char()
    kode_pelanggan = fields.Char()
    no_faktur = fields.Char()
    jenis_transaksi = fields.Char()
    jenis_pembayaran = fields.Char()
    kredit_lunak = fields.Char()
    jenis_faktur = fields.Char()
    no_reff_retur = fields.Char()
    no_referensi = fields.Char()
    id_program_diskon = fields.Char()
    id_program_promosi = fields.Char()
    id_program_voucher = fields.Char()
    sales_depo = fields.Char()
    ket_retur = fields.Char()
    status_barang = fields.Char()
    kode_promosi_principal = fields.Char()
    kode_rayon_kolektor = fields.Char()
    no_delivery = fields.Char()
    no_faktur_pajak = fields.Char()
    kc_promosi = fields.Char()

    # Float fields for numeric data
    sp_total_harga = fields.Float()
    sp_ppn = fields.Float()
    sp_diskon = fields.Float()
    sp_potongan = fields.Float()
    unitprice = fields.Float()
    qtyorder = fields.Float()
    qtyterpenuhi = fields.Float()
    diskonsp1 = fields.Float()
    diskonsp2 = fields.Float()
    hargasat_terbesar = fields.Float()
    hargasat_terkecil = fields.Float()
    qty_faktur = fields.Float()
    hargasat_faktur = fields.Float()
    qty_purchase_level = fields.Float()
    hargasat_purchase_level = fields.Float()
    qty_YJual_terkecil = fields.Float()
    hargasat_YJual_terkecil = fields.Float()
    gross = fields.Float()
    diskon1 = fields.Float()
    diskon2 = fields.Float()
    cash_diskon = fields.Float()
    potongan = fields.Float()
    netto = fields.Float()
    harga_mtc = fields.Float()
    harga_ttc = fields.Float()
    gross_pricelist = fields.Float()
    harga_penyetaraan = fields.Float()
    bsp_diskon_khusus = fields.Float()
    principal_diskon_khusus = fields.Float()
    principal_cn = fields.Float()
    bsp_cn = fields.Float()
    tonase = fields.Float()
    kubikasi = fields.Float()
    bsp_share = fields.Float()
    principal_share = fields.Float()
    gross_faktur = fields.Float()
    total_faktur = fields.Float()
    prc_prosen_diskon1 = fields.Float()
    prc_value_diskon1 = fields.Float()
    prc_prosen_diskon2 = fields.Float()
    prc_value_diskon2 = fields.Float()
    prc_prosen_diskon3 = fields.Float()
    prc_value_diskon3 = fields.Float()
    prc_prosen_diskon4 = fields.Float()
    prc_value_diskon4 = fields.Float()
    prc_prosen_diskon5 = fields.Float()
    prc_value_diskon5 = fields.Float()
    total_bayar = fields.Float()
    diskon_headerfk = fields.Float()
    potongan_headerfk = fields.Float()
    hna = fields.Float()
    sub_total = fields.Float()
    diskon_item = fields.Float()
    extra = fields.Float()
    cash_diskon_recalculate = fields.Float()
    nom_ppn = fields.Float()
    ppn_td_std = fields.Float()
    ppn_td_sdrhn = fields.Float()
    bebas_ppn_std = fields.Float()
    bebas_ppn_sdrhn = fields.Float()
    jml_pajak = fields.Float()

    # Date fields for date data
    tgl_referensi_order = fields.Date()
    podate = fields.Date()
    tglpomanual = fields.Date()
    tgledsp = fields.Date()
    tgl_faktur = fields.Date()
    tgl_jatuh_tempo = fields.Date()
    tgl_permintaan_kirim = fields.Date()
    delivery_date = fields.Date()
    tgl_mulai_overdue = fields.Date()
    tgl_referensi = fields.Date()
    tgl_faktur_pajak = fields.Date()
    kadaluarsa = fields.Date()
    last_update = fields.Datetime()

    fetch_date = fields.Date()
    km_index = fields.Char()

    # Automated method for Get Konsolidasi Master data 
    def cron_get_konsolidasi_master_per_batch(self):
        base_url = "http://192.168.16.130/microservice_internal/bis-pivot/bis/getKonsolidasi/?kode_cabang={}"

        for branch_name, abbreviation in list_cabang.items():
            current_ext_url = base_url.format(abbreviation.upper())


            print(f'Cronjob is currently requesting data for branch: {branch_name}, with abbreviation: {abbreviation}, URL: {current_ext_url}')   

            try:
                response = requests.get(current_ext_url)
                response.raise_for_status()

                if response.status_code != 200:
                    print(f"External Konsolidasi Master endpoint for branch {branch_name} didn't respond with status 200")
                else:
                    print(f"Konsolidasi Master data for branch {branch_name} successfully retrieved by cronjob")

            except requests.exceptions.RequestException as err:
                error_message = f"Error during GET request: {err}"
                print(error_message)
                _logger.error(error_message)