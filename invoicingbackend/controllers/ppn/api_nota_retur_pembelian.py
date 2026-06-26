from odoo import http
from odoo.http import request

class ApiNotaReturPembelian(http.Controller):

    @http.route('/api/nota-retur-pembelian/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_nota_retur_pembelian(self, **kw):
        try:
            records = request.env['invoicingbackend.nota_retur_pembelian'].search([])
            data = []
            for r in records:
                lines = []
                for l in r.line_ids:
                    lines.append({
                        'id': l.id,
                        'item_id': l.item_id.id if l.item_id else None,
                        'kode_barang': l.item_id.kode if l.item_id else '',
                        'nama_barang': l.nama_barang or '',
                        'satuan': l.satuan or '',
                        'kuantum': l.kuantum,
                        'harga_satuan': l.harga_satuan,
                        'harga_jual': l.harga_jual
                    })
                
                data.append({
                    'id': r.id,
                    'no_nota': r.no_nota or '',
                    'tgl_nota': r.tgl_nota.strftime('%Y-%m-%d') if r.tgl_nota else '',
                    'supplier_id': r.supplier_id.id if r.supplier_id else None,
                    'supplier_nama': r.supplier_id.nama if r.supplier_id else '',
                    'alamat_penjual': r.alamat_penjual or '',
                    'jenis_retur': r.jenis_retur or '',
                    'gudang_id': r.gudang_id or '',
                    'atas_no_fp': r.atas_no_fp or '',
                    'tgl_fp': r.tgl_fp.strftime('%Y-%m-%d') if r.tgl_fp else '',
                    'mata_uang_id': r.mata_uang_id.id if r.mata_uang_id else None,
                    'mata_uang_kode': r.mata_uang_id.kode if r.mata_uang_id else '',
                    'kurs_pajak': r.kurs_pajak,
                    'tarif_ppn': r.tarif_ppn,
                    'jenis_transaksi': r.jenis_transaksi or '',
                    'status': r.status or '',
                    'tanda_tangan': r.tanda_tangan or '',
                    'jabatan': r.jabatan or '',
                    'lines': lines
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/nota-retur-pembelian/create', type='json', auth='user', methods=['POST'], cors='*')
    def create_nota_retur_pembelian(self, **kw):
        try:
            params = kw
            lines_data = []
            if 'lines' in params:
                for line in params['lines']:
                    lines_data.append((0, 0, {
                        'item_id': line.get('item_id'),
                        'nama_barang': line.get('nama_barang'),
                        'satuan': line.get('satuan'),
                        'kuantum': line.get('kuantum'),
                        'harga_satuan': line.get('harga_satuan'),
                        'harga_jual': line.get('harga_jual')
                    }))
            
            val = {
                'no_nota': params.get('no_nota'),
                'tgl_nota': params.get('tgl_nota'),
                'supplier_id': params.get('supplier_id'),
                'alamat_penjual': params.get('alamat_penjual'),
                'jenis_retur': params.get('jenis_retur'),
                'gudang_id': params.get('gudang_id'),
                'atas_no_fp': params.get('atas_no_fp'),
                'tgl_fp': params.get('tgl_fp') or False,
                'mata_uang_id': params.get('mata_uang_id'),
                'kurs_pajak': params.get('kurs_pajak'),
                'tarif_ppn': params.get('tarif_ppn'),
                'jenis_transaksi': params.get('jenis_transaksi'),
                'status': params.get('status'),
                'tanda_tangan': params.get('tanda_tangan'),
                'jabatan': params.get('jabatan'),
                'line_ids': lines_data
            }
            
            if params.get('id'):
                record = request.env['invoicingbackend.nota_retur_pembelian'].browse(params['id'])
                record.line_ids.unlink()
                record.write(val)
                res_id = record.id
            else:
                val['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.nota_retur_pembelian'].create(val)
                res_id = record.id
                
            return {'status': 'success', 'id': res_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/nota-retur-pembelian/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_nota_retur_pembelian(self, **kw):
        try:
            record_id = kw.get('id')
            if record_id:
                request.env['invoicingbackend.nota_retur_pembelian'].browse(record_id).unlink()
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/nota-retur-pembelian/autono', type='json', auth='user', methods=['POST'], cors='*')
    def autono_nota_retur_pembelian(self, **kw):
        return {'status': 'success', 'no_nota': 'RB/00X/03/2026'}
