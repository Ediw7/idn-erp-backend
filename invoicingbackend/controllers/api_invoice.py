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

                surat_jalans_data = []
                for sj in rec.surat_jalan_ids:
                    surat_jalans_data.append({
                        'no_sj': sj.no_sj,
                        'tanggal': sj.tgl_sj.strftime('%Y-%m-%d') if sj.tgl_sj else '',
                        'keterangan': sj.keterangan or ''
                    })
                
                # Legacy fallback just in case
                if not surat_jalans_data and rec.surat_jalan_id:
                    surat_jalans_data.append({
                        'no_sj': rec.surat_jalan_id.no_sj,
                        'tanggal': rec.surat_jalan_id.tgl_sj.strftime('%Y-%m-%d') if rec.surat_jalan_id.tgl_sj else '',
                        'keterangan': rec.surat_jalan_id.keterangan or ''
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
                    'surat_jalans': surat_jalans_data,
                    'no_sj': rec.surat_jalan_id.no_sj if rec.surat_jalan_id else (surat_jalans_data[0]['no_sj'] if surat_jalans_data else ''),
                    'sales_order_id': rec.sales_order_id.id if rec.sales_order_id else '',
                    'no_so': rec.sales_order_id.no_so if rec.sales_order_id else '',
                    'no_fp': rec.no_fp or '',
                    'tgl_fp': str(rec.tgl_fp) if rec.tgl_fp else '',
                    'keterangan': rec.keterangan or '',
                    'potongan_harga': rec.potongan_harga or 0.0,
                    'ppn_persen': rec.ppn_persen or 0.0,
                    'ppn_amount': rec.ppn_amount or 0.0,
                    'pph_persen': rec.pph_persen or 0.0,
                    'pph_amount': rec.pph_amount or 0.0,
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
            
            surat_jalans = data.get('surat_jalans', [])
            found_sjs = request.env['invoicingbackend.surat_jalan']
            
            # Support multiple SJs
            if surat_jalans and isinstance(surat_jalans, list):
                sj_nos = [sj.get('no_sj') for sj in surat_jalans if sj.get('no_sj')]
                if sj_nos:
                    found_sjs = request.env['invoicingbackend.surat_jalan'].search([('no_sj', 'in', sj_nos)])
            
            # Validasi apakah SJ ini sudah di-invoice oleh dokumen lain
            if found_sjs:
                existing_domain = [
                    ('invoice_id', '!=', False),
                    ('is_void', '=', False),
                    ('id', 'in', found_sjs.ids)
                ]
                if invoice_id:
                    existing_domain.append(('invoice_id', '!=', int(invoice_id)))
                    
                existing = request.env['invoicingbackend.surat_jalan'].search_count(existing_domain)
                if existing > 0:
                    return ApiResponse.error(message="Salah satu Surat Jalan ini sudah pernah ditagihkan (Di-Invoice). Tidak bisa dibuat double!", status_code=400)

            vals = {
                'no_invoice': data.get('no_invoice'),
                'tgl_invoice': data.get('tgl_invoice'),
                'pelanggan_id': data.get('pelanggan_id'),
                'surat_jalan_ids': [(6, 0, found_sjs.ids)] if found_sjs else False,
                'surat_jalan_id': found_sjs[0].id if len(found_sjs) > 0 else False, # Fallback legacy
                'sales_order_id': data.get('sales_order_id'),
                'no_fp': data.get('no_fp'),
                'tgl_fp': data.get('tgl_fp') or False,
                'keterangan': data.get('keterangan'),
                'potongan_harga': float(data.get('potongan_harga', 0.0)),
                'ppn_persen': float(data.get('ppn_persen', 0.0)),
                'pph_persen': float(data.get('pph_persen', 0.0)),
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
                
            # Update Surat Jalan terkait: Kosongkan yang lama (jika ada), isi yang baru
            if invoice_id:
                # Cari SJ yang mungkin dilepas dari invoice ini dan kosongkan
                orphaned_sjs = request.env['invoicingbackend.surat_jalan'].search([
                    ('no_invoice', '=', record.no_invoice),
                    ('id', 'not in', found_sjs.ids)
                ])
                if orphaned_sjs:
                    orphaned_sjs.write({'no_invoice': '', 'invoice_id': False})
            
            if found_sjs:
                found_sjs.write({'no_invoice': record.no_invoice, 'invoice_id': record.id})

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
                if record.total_terbayar > 0:
                    return ApiResponse.error(message='Invoice tidak dapat dihapus karena sudah memiliki riwayat pembayaran!', status_code=400)
                
                # Kosongkan no_invoice pada Surat Jalan terkait sebelum di-delete
                if record.surat_jalan_ids:
                    record.surat_jalan_ids.write({'no_invoice': '', 'invoice_id': False})
                elif record.surat_jalan_id:
                    record.surat_jalan_id.write({'no_invoice': '', 'invoice_id': False})
                    
                record.unlink()
                return ApiResponse.success(message='Invoice berhasil dihapus')
            return ApiResponse.error(message='Data tidak ditemukan', status_code=404)
        except Exception as e:
            _logger.error(f"Error deleting invoice: {str(e)}")
            return ApiResponse.error(message=str(e), status_code=500)
