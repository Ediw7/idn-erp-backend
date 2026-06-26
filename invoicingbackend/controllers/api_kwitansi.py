from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
import logging

_logger = logging.getLogger(__name__)

class ApiKwitansi(http.Controller):

    @http.route('/api/kwitansi/get', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_kwitansi(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            domain = [('company_id', '=', request.env.user.company_id.id)]
            limit = int(kwargs.get('limit', 2000))
            records = request.env['invoicingbackend.kwitansi'].search(domain, order='tgl_kwitansi desc', limit=limit)
            
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_kwitansi': rec.no_kwitansi,
                    'tgl_kwitansi': str(rec.tgl_kwitansi) if rec.tgl_kwitansi else '',
                    'jenis': rec.jenis or '',
                    'invoice_id': rec.invoice_id.id if rec.invoice_id else None,
                    'invoice_no': rec.invoice_id.no_invoice if rec.invoice_id else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else None,
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'mata_uang': rec.mata_uang or 'IDR',
                    'jumlah': rec.jumlah,
                    'terbilang': rec.terbilang or '',
                    'untuk_pembayaran': rec.untuk_pembayaran or '',
                    'penandatangan': rec.penandatangan or '',
                    'jabatan': rec.jabatan or '',
                })
            return ApiResponse.success(data=data)
        except Exception as e:
            _logger.error(f"Error fetching kwitansi: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/kwitansi/save', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def save_kwitansi(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            kw_id = data.get('id')
            
            vals = {
                'no_kwitansi': data.get('no_kwitansi'),
                'tgl_kwitansi': data.get('tgl_kwitansi'),
                'jenis': data.get('jenis', 'VAT'),
                'invoice_id': data.get('invoice_id'),
                'pelanggan_id': data.get('pelanggan_id'),
                'mata_uang': data.get('mata_uang', 'IDR'),
                'jumlah': float(data.get('jumlah', 0.0)),
                'terbilang': data.get('terbilang'),
                'untuk_pembayaran': data.get('untuk_pembayaran'),
                'keterangan_footer': data.get('keterangan_footer'),
                'penandatangan': data.get('penandatangan'),
                'jabatan': data.get('jabatan'),
                'company_id': request.env.user.company_id.id,
            }

            if kw_id:
                record = request.env['invoicingbackend.kwitansi'].browse(kw_id)
                if record.exists():
                    record.write(vals)
                else:
                    return ApiResponse.error(message='Data Kwitansi tidak ditemukan', status_code=404)
            else:
                record = request.env['invoicingbackend.kwitansi'].create(vals)
                
            return ApiResponse.success(data={'id': record.id}, message='Kwitansi berhasil disimpan')
            
        except Exception as e:
            _logger.error(f"Error saving kwitansi: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
