from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
import logging

_logger = logging.getLogger(__name__)

class ApiSuratJalan(http.Controller):

    @http.route('/api/surat_jalan/get', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_surat_jalan(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            domain = [('company_id', '=', request.env.user.company_id.id)]
            limit = int(kwargs.get('limit', 2000))
            records = request.env['invoicingbackend.surat_jalan'].search(domain, order='tgl_sj desc', limit=limit)
            
            data = []
            for rec in records:
                lines = []
                for line in rec.line_ids:
                    lines.append({
                        'item_id': line.item_id.id if line.item_id else None,
                        'kode': line.item_id.kode if line.item_id else '',
                        'nama': line.nama_barang or '',
                        'satuan': line.satuan or '',
                        'kuantum': line.kuantum,
                        'keterangan': line.keterangan or ''
                    })
                
                data.append({
                    'id': rec.id,
                    'no_sj': rec.no_sj or '',
                    'tanggal': rec.tgl_sj.strftime('%Y-%m-%d') if rec.tgl_sj else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else '',
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'alamat_kirim': rec.alamat_kirim or '',
                    'gudang_id': rec.gudang_id.id if rec.gudang_id else '',
                    'no_so': rec.so_id.no_so if rec.so_id else '',
                    'so_id': rec.so_id.id if rec.so_id else '',
                    'no_po': rec.no_po or '',
                    'no_kendaraan': rec.no_kendaraan or '',
                    'no_invoice': rec.no_invoice or '',
                    'keterangan': rec.keterangan or '',
                    'lines': lines,
                })
            return ApiResponse.success(data=data)
        except Exception as e:
            _logger.error(f"Error fetching surat jalan: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/surat_jalan/save', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def save_surat_jalan(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            sj_id = data.get('id')
            
            # --- Validasi Data Wajib ---
            if not data.get('no_sj'):
                return ApiResponse.error(message='Nomor Surat Jalan wajib diisi.', status_code=400)
            if not data.get('tgl_sj'):
                return ApiResponse.error(message='Tanggal Surat Jalan wajib diisi.', status_code=400)
            if not data.get('pelanggan_id'):
                return ApiResponse.error(message='Nama Pelanggan wajib dipilih.', status_code=400)
            
            vals = {
                'no_sj': data.get('no_sj'),
                'tgl_sj': data.get('tgl_sj'),
                'pelanggan_id': data.get('pelanggan_id'),
                'alamat_kirim': data.get('alamat_kirim'),
                'gudang_id': data.get('gudang_id'),
                'so_id': data.get('so_id'),
                'no_po': data.get('no_po'),
                'no_kendaraan': data.get('no_kendaraan'),
                'keterangan': data.get('keterangan'),
                'company_id': request.env.user.company_id.id,
            }

            lines_data = data.get('lines', [])
            line_cmds = []
            
            if sj_id:
                line_cmds.append((5, 0, 0)) # Clear existing lines
                
            for line in lines_data:
                line_cmds.append((0, 0, {
                    'item_id': line.get('item_id'),
                    'satuan': line.get('satuan', ''),
                    'kuantum': float(line.get('kuantum', 1.0)),
                    'keterangan': line.get('keterangan', ''),
                    'company_id': request.env.user.company_id.id,
                }))
                
            vals['line_ids'] = line_cmds

            if sj_id:
                record = request.env['invoicingbackend.surat_jalan'].browse(sj_id)
                if record.exists():
                    record.write(vals)
                else:
                    return ApiResponse.error(message='Data Surat Jalan tidak ditemukan', status_code=404)
            else:
                record = request.env['invoicingbackend.surat_jalan'].create(vals)
                
            return ApiResponse.success(data={'id': record.id}, message='Surat Jalan berhasil disimpan')
            
        except Exception as e:
            _logger.error(f"Error saving surat jalan: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/surat_jalan/delete', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def delete_surat_jalan(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            sj_id = data.get('id')
            if not sj_id:
                return ApiResponse.error(message='ID Surat Jalan tidak ditemukan.', status_code=400)
            record = request.env['invoicingbackend.surat_jalan'].browse(int(sj_id))
            if record.exists():
                record.unlink()
                return ApiResponse.success(message='Surat Jalan berhasil dihapus')
            return ApiResponse.error(message='Data tidak ditemukan', status_code=404)
        except Exception as e:
            _logger.error(f"Error deleting surat jalan: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
