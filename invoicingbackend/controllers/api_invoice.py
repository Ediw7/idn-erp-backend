from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
import logging

_logger = logging.getLogger(__name__)

class ApiInvoice(http.Controller):

    @http.route('/api/invoice/get', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_invoices(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            domain = [('company_id', '=', request.env.user.company_id.id)]
            limit = int(kwargs.get('limit', 2000))
            records = request.env['invoicingbackend.invoice'].search(domain, order='tgl_invoice desc', limit=limit)
            
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_invoice': rec.no_invoice,
                    'tgl_invoice': str(rec.tgl_invoice) if rec.tgl_invoice else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else None,
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'surat_jalan_id': rec.surat_jalan_id.id if rec.surat_jalan_id else None,
                    'no_fp': rec.no_fp or '',
                    'total': rec.total,
                    'total_terbayar': rec.total_terbayar,
                    'saldo_piutang': rec.saldo_piutang,
                    'is_lunas': rec.is_lunas,
                    'is_void': rec.is_void,
                })
            return ApiResponse.success(data=data)
        except Exception as e:
            _logger.error(f"Error fetching invoices: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/invoice/save', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def save_invoice(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            invoice_id = data.get('id')
            
            vals = {
                'no_invoice': data.get('no_invoice'),
                'tgl_invoice': data.get('tgl_invoice'),
                'pelanggan_id': data.get('pelanggan_id'),
                'surat_jalan_id': data.get('surat_jalan_id'),
                'sales_order_id': data.get('sales_order_id'),
                'no_fp': data.get('no_fp'),
                'tgl_fp': data.get('tgl_fp') or False,
                'keterangan': data.get('keterangan'),
                'potongan_harga': float(data.get('potongan_harga', 0.0)),
                'ppn_persen': float(data.get('ppn_persen', 11.0)),
                'ongkos_angkut': float(data.get('ongkos_angkut', 0.0)),
                'company_id': request.env.user.company_id.id,
            }

            # Detail lines
            lines_data = data.get('lines', [])
            line_cmds = []
            
            # Kita bersihkan lines lama jika ini update (bisa di-improve dengan pencocokan ID)
            if invoice_id:
                line_cmds.append((5, 0, 0)) # Clear existing lines
                
            for line in lines_data:
                line_cmds.append((0, 0, {
                    'item_id': line.get('item_id'),
                    'kuantum': float(line.get('kuantum', 1.0)),
                    'harga_satuan': float(line.get('harga_satuan', 0.0)),
                    'disc_persen': float(line.get('disc_persen', 0.0)),
                    'disc_harga': float(line.get('disc_harga', 0.0)),
                    'company_id': request.env.user.company_id.id,
                }))
                
            vals['line_ids'] = line_cmds

            if invoice_id:
                record = request.env['invoicingbackend.invoice'].browse(invoice_id)
                if record.exists():
                    if record.is_void:
                        return ApiResponse.error(message="Tidak dapat merubah invoice yang sudah di-void", status_code=400)
                    record.write(vals)
                else:
                    return ApiResponse.error(message='Data Invoice tidak ditemukan', status_code=404)
            else:
                record = request.env['invoicingbackend.invoice'].create(vals)
                
            return ApiResponse.success(data={'id': record.id}, message='Invoice berhasil disimpan')
            
        except Exception as e:
            _logger.error(f"Error saving invoice: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
