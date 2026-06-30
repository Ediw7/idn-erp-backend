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
                lines = []
                for line in rec.line_ids:
                    lines.append({
                        'item_id': line.item_id.id if line.item_id else None,
                        'kode': line.item_id.kode if line.item_id else '',
                        'nama': line.nama_barang or '',
                        'satuan': line.satuan or '',
                        'kuantum': line.kuantum,
                        'harga_satuan': line.harga_satuan,
                        'disc_persen': line.disc_persen,
                        'disc_harga': line.disc_harga,
                        'harga_jual': line.harga_jual,
                    })

                data.append({
                    'id': rec.id,
                    'no_invoice': rec.no_invoice or '',
                    'tgl_invoice': str(rec.tgl_invoice) if rec.tgl_invoice else '',
                    'pembeli_id': rec.pelanggan_id.id if rec.pelanggan_id else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else '',
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'alamat': rec.pelanggan_id.alamat_wp or rec.pelanggan_id.alamat or '',
                    'npwp': rec.pelanggan_id.npwp or '',
                    'surat_jalan_id': rec.surat_jalan_id.id if rec.surat_jalan_id else '',
                    'sales_order_id': rec.sales_order_id.id if rec.sales_order_id else '',
                    'no_so': rec.sales_order_id.no_so if rec.sales_order_id else '',
                    'no_fp': rec.no_fp or '',
                    'tgl_fp': str(rec.tgl_fp) if rec.tgl_fp else '',
                    'keterangan': rec.keterangan or '',
                    'potongan_harga': rec.potongan_harga or 0.0,
                    'ppn_persen': rec.ppn_persen or 0.0,
                    'ongkos_angkut': rec.ongkos_angkut or 0.0,
                    'total': rec.total,
                    'total_terbayar': rec.total_terbayar,
                    'saldo_piutang': rec.saldo_piutang,
                    'is_lunas': rec.is_lunas,
                    'is_void': rec.is_void,
                    'lines': lines,
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
            
            if not data.get('no_invoice'):
                return ApiResponse.error(message='Nomor Invoice wajib diisi.', status_code=400)
            if not data.get('tgl_invoice'):
                return ApiResponse.error(message='Tanggal Invoice wajib diisi.', status_code=400)
            if not data.get('pelanggan_id'):
                return ApiResponse.error(message='Pelanggan wajib dipilih.', status_code=400)
            
            surat_jalan_id = data.get('surat_jalan_id')
            if not surat_jalan_id and data.get('surat_jalans'):
                # Coba cari dari data 'surat_jalans' array
                no_sj = data.get('surat_jalans')[0].get('no_sj') if isinstance(data.get('surat_jalans'), list) and len(data.get('surat_jalans')) > 0 else None
                if no_sj:
                    sj = request.env['invoicingbackend.surat_jalan'].search([('no_sj', '=', no_sj)], limit=1)
                    if sj:
                        surat_jalan_id = sj.id

            if surat_jalan_id:
                # Cek apakah SJ ini sudah di-invoice oleh dokumen lain (yang bukan void)
                existing_domain = [
                    ('surat_jalan_id', '=', surat_jalan_id),
                    ('is_void', '=', False)
                ]
                if invoice_id:
                    existing_domain.append(('id', '!=', int(invoice_id)))
                    
                existing = request.env['invoicingbackend.invoice'].search_count(existing_domain)
                if existing > 0:
                    return ApiResponse.error(message="Surat Jalan ini sudah pernah ditagihkan (Di-Invoice). Tidak bisa dibuat double!", status_code=400)

            vals = {
                'no_invoice': data.get('no_invoice'),
                'tgl_invoice': data.get('tgl_invoice'),
                'pelanggan_id': data.get('pelanggan_id'),
                'surat_jalan_id': surat_jalan_id,
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
                record = request.env['invoicingbackend.invoice'].browse(int(invoice_id))
                if record.exists():
                    if record.is_void:
                        return ApiResponse.error(message="Tidak dapat merubah invoice yang sudah di-void", status_code=400)
                    if record.total_terbayar > 0:
                        return ApiResponse.error(message="Invoice sudah memiliki riwayat pembayaran, tidak dapat diedit!", status_code=400)
                    
                    record.write(vals)
                else:
                    return ApiResponse.error(message='Data Invoice tidak ditemukan', status_code=404)
            else:
                record = request.env['invoicingbackend.invoice'].create(vals)
                
            # Update Surat Jalan terkait
            if surat_jalan_id:
                sj = request.env['invoicingbackend.surat_jalan'].browse(surat_jalan_id)
                if sj.exists():
                    sj.write({'no_invoice': record.no_invoice})

            return ApiResponse.success(data={'id': record.id}, message='Invoice berhasil disimpan')
            
        except Exception as e:
            _logger.error(f"Error saving invoice: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/invoice/delete', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def delete_invoice(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            invoice_id = data.get('id')
            if not invoice_id:
                return ApiResponse.error(message='ID Invoice tidak ditemukan.', status_code=400)
            record = request.env['invoicingbackend.invoice'].browse(int(invoice_id))
            if record.exists():
                if record.is_lunas:
                    return ApiResponse.error(message='Invoice sudah lunas tidak dapat dihapus', status_code=400)
                if record.total_terbayar > 0:
                    return ApiResponse.error(message='Invoice tidak dapat dihapus karena sudah memiliki riwayat pembayaran (walaupun belum lunas)!', status_code=400)
                
                # Kosongkan no_invoice pada Surat Jalan terkait sebelum di-delete
                if record.surat_jalan_id:
                    record.surat_jalan_id.write({'no_invoice': ''})
                    
                record.unlink()
                return ApiResponse.success(message='Invoice berhasil dihapus')
            return ApiResponse.error(message='Data tidak ditemukan', status_code=404)
        except Exception as e:
            _logger.error(f"Error deleting invoice: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
