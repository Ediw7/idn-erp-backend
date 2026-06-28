from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
import logging

_logger = logging.getLogger(__name__)

class ApiPembayaranPiutang(http.Controller):

    @http.route('/api/pembayaran/get', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_pembayaran(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            domain = [('company_id', '=', request.env.user.company_id.id)]
            limit = int(kwargs.get('limit', 2000))
            records = request.env['invoicingbackend.pembayaran_piutang'].search(domain, order='tgl_pembayaran desc', limit=limit)
            
            data = []
            for rec in records:
                lines = []
                for line in rec.line_ids:
                    lines.append({
                        'invoice_id': line.invoice_id.id if line.invoice_id else '',
                        'no_invoice': line.invoice_id.no_invoice if line.invoice_id else '',
                        'no_faktur_pajak': line.invoice_id.no_fp if line.invoice_id else '',
                        'tgl_jt': '',
                        'ccy': 'IDR',
                        'saldo_piutang': line.invoice_id.saldo_piutang + line.pembayaran if line.invoice_id else 0, # rough estimate before save
                        'pembayaran': line.pembayaran,
                        'potongan': line.potongan,
                        'keterangan': line.keterangan or ''
                    })

                data.append({
                    'id': rec.id,
                    'no_bukti': rec.no_bukti or '',
                    'tanggal': str(rec.tgl_pembayaran) if rec.tgl_pembayaran else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else '',
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'alamat': rec.pelanggan_id.alamat_wp or rec.pelanggan_id.alamat or '',
                    'perkiraan_kas_bank': rec.perkiraan_kas_id.id if rec.perkiraan_kas_id else '',
                    'keterangan': rec.keterangan or '',
                    'metode_pembayaran': 'Transfer',
                    'no_cek_giro': '',
                    'tanggal_cair': '',
                    'mata_uang': 'IDR',
                    'jumlah_penerimaan': rec.total_pembayaran,
                    'total_potongan': rec.total_potongan,
                    'is_void': rec.is_void,
                    'lines': lines,
                })
            return ApiResponse.success(data=data)
        except Exception as e:
            _logger.error(f"Error fetching pembayaran: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/pembayaran/save', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def save_pembayaran(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            pem_id = data.get('id')
            
            vals = {
                'no_bukti': data.get('no_bukti'),
                'tgl_pembayaran': data.get('tgl_pembayaran'),
                'pelanggan_id': data.get('pelanggan_id'),
                'perkiraan_kas_id': data.get('perkiraan_kas_id'),
                'keterangan': data.get('keterangan'),
                'company_id': request.env.user.company_id.id,
            }

            lines_data = data.get('lines', [])
            line_cmds = []
            
            if pem_id:
                line_cmds.append((5, 0, 0)) # Clear existing lines
                
            for line in lines_data:
                # Validasi saldo dsb bisa dilakukan di sisi Odoo Model atau sini.
                # Karena model pembayaran_piutang_line pakai constrains, kita insert saja.
                line_cmds.append((0, 0, {
                    'invoice_id': line.get('invoice_id'),
                    'pembayaran': float(line.get('pembayaran', 0.0)),
                    'potongan': float(line.get('potongan', 0.0)),
                    'keterangan': line.get('keterangan', ''),
                    'company_id': request.env.user.company_id.id,
                }))
                
            vals['line_ids'] = line_cmds

            if pem_id:
                record = request.env['invoicingbackend.pembayaran_piutang'].browse(pem_id)
                if record.exists():
                    if record.is_void:
                        return ApiResponse.error(message="Tidak dapat merubah pembayaran yang sudah di-void", status_code=400)
                    record.write(vals)
                else:
                    return ApiResponse.error(message='Data Pembayaran tidak ditemukan', status_code=404)
            else:
                record = request.env['invoicingbackend.pembayaran_piutang'].create(vals)
                
            return ApiResponse.success(data={'id': record.id}, message='Pembayaran berhasil disimpan')
            
        except Exception as e:
            _logger.error(f"Error saving pembayaran: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/pembayaran/delete', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def delete_pembayaran(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            pem_id = data.get('id')
            if not pem_id:
                return ApiResponse.error(message='ID Pembayaran tidak ditemukan.', status_code=400)
            record = request.env['invoicingbackend.pembayaran_piutang'].browse(int(pem_id))
            if record.exists():
                if record.is_void:
                    return ApiResponse.error(message='Pembayaran sudah di-void tidak dapat dihapus', status_code=400)
                record.unlink()
                return ApiResponse.success(message='Pembayaran berhasil dihapus')
            return ApiResponse.error(message='Data tidak ditemukan', status_code=404)
        except Exception as e:
            _logger.error(f"Error deleting pembayaran: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
