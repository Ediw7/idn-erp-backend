from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
import logging

_logger = logging.getLogger(__name__)

class ApiOutstanding(http.Controller):

    @http.route('/api/outstanding/get', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_outstanding(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            domain = [
                ('company_id', '=', request.env.user.company_id.id),
                ('saldo_piutang', '>', 0),
                ('is_void', '=', False)
            ]
            
            # Kita bisa memfilter berdasarkan pelanggan_id jika dikirim lewat params
            pelanggan_id = kwargs.get('pelanggan_id')
            if pelanggan_id:
                domain.append(('pelanggan_id', '=', int(pelanggan_id)))

            limit = int(kwargs.get('limit', 2000))
            records = request.env['invoicingbackend.invoice'].search(domain, order="tgl_invoice ASC", limit=limit)
            
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_invoice': rec.no_invoice,
                    'tgl_invoice': str(rec.tgl_invoice) if rec.tgl_invoice else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else None,
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'total_tagihan': rec.total,
                    'total_terbayar': rec.total_terbayar,
                    'saldo_piutang': rec.saldo_piutang,
                })
            return ApiResponse.success(data=data)
        except Exception as e:
            _logger.error(f"Error fetching outstanding: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
