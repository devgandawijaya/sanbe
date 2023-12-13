from odoo import http
from odoo.http import request, content_disposition
import logging
import io
import xlsxwriter
from requests.exceptions import ConnectionError, RequestException

_logger = logging.getLogger(__name__)

class PivotStockController(http.Controller):
    
    @http.route('/pivot-stock-import', type='http', auth='public', csrf=False)
    def import_konsolidasi_cocba(self, **kwargs):
        data_stock_model = request.env['daily.stock'].sudo()
        pivot_stock_model = request.env['pivot.stock'].sudo()

        konsolidasi_data = data_stock_model.search([])
        query = """
            SELECT tgl_stock, kode_cabang, kode_principal, "Kode_Divisi_Produk_id", nama_barang_id, kode_barang,
            SUM(rev_ssl) AS ssl_data, SUM(avail_akhir) AS STOCK
            FROM daily_stock
            WHERE kode_cabang IN ('BLG','BDG')
            GROUP BY tgl_stock, kode_cabang, kode_principal, "Kode_Divisi_Produk_id", nama_barang_id, kode_barang;
        """

        request.env.cr.execute(query)
        result = request.env.cr.fetchall()
        for rec in result:
            tgl_stock, kode_cabang, kode_principal, kode_divisi_produk_id, nama_barang_id, kode_barang, ssl_data, stock = rec
            existing_record = pivot_stock_model.search([
                ('tgl_stock', '=', tgl_stock),
                ('kode_cabang', '=', kode_cabang),
                ('kode_principal', '=', kode_principal),
                ('Kode_Divisi_Produk_id', '=', kode_divisi_produk_id),
                ('nama_barang_id', '=', nama_barang_id),
                ('kode_barang', '=', kode_barang),
            ], limit=1)
            if not existing_record:
                pivot_stock_model.create({
                    'tgl_stock': tgl_stock,
                    'kode_cabang': kode_cabang,
                    'kode_principal': kode_principal,
                    'Kode_Divisi_Produk_id': kode_divisi_produk_id,
                    'nama_barang_id': nama_barang_id,
                    'kode_barang': kode_barang,
                    'rev_ssl': ssl_data,
                    'avail_akhir': stock,
                })
                request.env.cr.commit()
        
        action = request.env['ir.actions.act_window'].sudo().search([('name', '=', 'Pivot Stock')], limit=1)
        action_id = action.id if action else None

        menu = request.env['ir.ui.menu'].sudo().search([('name', '=', 'Pivot Stock')], limit=1)
        menu_id = menu.id if menu else None

        return request.redirect(f'/web#action={action_id}&menu_id={menu_id}')

    @http.route('/pivot_stock/export_excel', type='http', auth="user")
    def export_data_replacing_excel(self, ids=None):
        record_ids = [int(id) for id in ids.split(',')] if ids else []

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Data Replacing')

        # Define the headers
        headers = [
            'Tanggal Stok', 'Kode Cabang', 'Kode Principal', 'Kode Barang Principal', 'Kode Divisi Produk', 'Kode Barang', 'Nama Barang', 'SSL', 'STOCK', 'RATIO'
        ]

        # Write the headers
        for i, header in enumerate(headers):
            worksheet.write(0, i, header)

        # Fetch the data
        if record_ids:
            pivot_stock_records = request.env['pivot.stock'].sudo().browse(record_ids)
        else:
            pivot_stock_records = request.env['pivot.stock'].sudo().search([])

        # Write data to Excel file
        row = 1
        for record in pivot_stock_records:
            worksheet.write(row, 0, record.tgl_stock.strftime('%d-%m-%Y') if record.tgl_stock else '')
            worksheet.write(row, 1, record.kode_cabang or '')
            worksheet.write(row, 2, record.kode_principal or '')
            worksheet.write(row, 3, record.kode_barang or '')  # Adjust field name if necessary
            worksheet.write(row, 4, record.Kode_Divisi_Produk_id or '')  # Adjust field name if necessary
            worksheet.write(row, 5, record.nama_barang_id or '')
            worksheet.write(row, 6, str(record.rev_ssl) if record.rev_ssl else '0')
            worksheet.write(row, 7, str(record.avail_akhir) if record.avail_akhir else '0')
            worksheet.write(row, 8, record.ratio or '0')
            row += 1

        workbook.close()
        output.seek(0)
        response = request.make_response(
            output.getvalue(),
            [('Content-Type', 'application/vnd.ms-excel'),
            ('Content-Disposition', content_disposition('pivot_stock_export.xlsx'))]
        )
        return response