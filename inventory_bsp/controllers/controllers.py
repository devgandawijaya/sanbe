# from odoo import http
# from odoo.http import request
# import logging

# _logger = logging.getLogger(__name__)

# class PaginationController(http.Controller):

#     @http.route('/update_product_konversi_page', type='http', auth='user')
#     def update_product_konversi_page(self, page, **kw):
#         # Update product conversion logic here
#         try:
#             page = int(page)
#             request.env['product.konversi'].with_context({'current_page': page}).update_product_konversi()
#             _logger.info(f"Current page is now: {page}")
#             return {'success': True}
#         except ValueError:
#             _logger.error("Invalid page number received")
#             return {'success': False, 'error': 'Invalid page number'}
