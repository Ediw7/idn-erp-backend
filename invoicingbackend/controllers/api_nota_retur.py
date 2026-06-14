from odoo import http
from odoo.http import request

class ApiNotaRetur(http.Controller):

    @http.route('/api/nota-retur/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_nota_retur(self, **kw):
        try:
            records = request.env['invoicingbackend.nota_retur'].search([])
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
                        'harga_jual': l.harga_jual,
                        'hpp': l.hpp,
                        'total_hpp': l.total_hpp
                    })
                
                data.append({
                    'id': r.id,
                    'no_nota': r.no_nota or '',
                    'tgl_nota': r.tgl_nota.strftime('%Y-%m-%d') if r.tgl_nota else '',
                    'pelanggan_id': r.pelanggan_id.id if r.pelanggan_id else None,
                    'pelanggan_nama': r.pelanggan_id.nama if r.pelanggan_id else '',
                    'alamat_pembeli': r.alamat_pembeli or '',
                    'jenis_transaksi': r.jenis_transaksi or '',
                    'gudang_id': r.gudang_id or '',
                    'jenis_retur': r.jenis_retur or '',
                    'atas_no_fp': r.atas_no_fp or '',
                    'tgl_fp': r.tgl_fp.strftime('%Y-%m-%d') if r.tgl_fp else '',
                    'atas_no_invoice': r.atas_no_invoice or '',
                    'mata_uang_id': r.mata_uang_id.id if r.mata_uang_id else None,
                    'mata_uang_kode': r.mata_uang_id.kode if r.mata_uang_id else '',
                    'tarif_ppn': r.tarif_ppn,
                    'kurs_pajak': r.kurs_pajak,
                    'lokasi_pelaporan': r.lokasi_pelaporan or '',
                    'tanda_tangan': r.tanda_tangan or '',
                    'jabatan': r.jabatan or '',
                    'lines': lines
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/nota-retur/create', type='json', auth='user', methods=['POST'], cors='*')
    def create_nota_retur(self, **kw):
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
                        'harga_jual': line.get('harga_jual'),
                        'hpp': line.get('hpp'),
                        'total_hpp': line.get('total_hpp')
                    }))
            
            val = {
                'no_nota': params.get('no_nota'),
                'tgl_nota': params.get('tgl_nota'),
                'pelanggan_id': params.get('pelanggan_id'),
                'alamat_pembeli': params.get('alamat_pembeli'),
                'jenis_transaksi': params.get('jenis_transaksi'),
                'gudang_id': params.get('gudang_id'),
                'jenis_retur': params.get('jenis_retur'),
                'atas_no_fp': params.get('atas_no_fp'),
                'tgl_fp': params.get('tgl_fp') or False,
                'atas_no_invoice': params.get('atas_no_invoice'),
                'mata_uang_id': params.get('mata_uang_id'),
                'tarif_ppn': params.get('tarif_ppn'),
                'kurs_pajak': params.get('kurs_pajak'),
                'lokasi_pelaporan': params.get('lokasi_pelaporan'),
                'tanda_tangan': params.get('tanda_tangan'),
                'jabatan': params.get('jabatan'),
                'line_ids': lines_data
            }
            
            if params.get('id'):
                record = request.env['invoicingbackend.nota_retur'].browse(params['id'])
                record.line_ids.unlink() # clear existing lines
                record.write(val)
                res_id = record.id
            else:
                record = request.env['invoicingbackend.nota_retur'].create(val)
                res_id = record.id
                
            return {'status': 'success', 'id': res_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/nota-retur/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_nota_retur(self, **kw):
        try:
            record_id = kw.get('id')
            if record_id:
                request.env['invoicingbackend.nota_retur'].browse(record_id).unlink()
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/nota-retur/autono', type='json', auth='user', methods=['POST'], cors='*')
    def autono_nota_retur(self, **kw):
        return {'status': 'success', 'no_nota': 'RJ/00X/03/2026'}
