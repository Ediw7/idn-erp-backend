from odoo import http
from odoo.http import request

class ApiSuratSetoranPajak(http.Controller):

    @http.route('/api/ssp/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_ssp(self, **kw):
        try:
            records = request.env['invoicingbackend.surat_setoran_pajak'].search([])
            data = []
            for r in records:
                data.append({
                    'id': r.id,
                    'kpp': r.kpp or '',
                    'nama_wp': r.nama_wp or '',
                    'npwp': r.npwp or '',
                    'alamat': r.alamat or '',
                    'kode_pos': r.kode_pos or '',
                    'tahun': r.tahun or '',
                    'bulan': r.bulan or '',
                    'kode_jenis_pajak': r.kode_jenis_pajak or '',
                    'kode_jenis_pajak_desc': r.kode_jenis_pajak_desc or '',
                    'kode_jenis_setoran': r.kode_jenis_setoran or '',
                    'kode_jenis_setoran_desc': r.kode_jenis_setoran_desc or '',
                    'uraian_pembayaran': r.uraian_pembayaran or '',
                    'no_ketetapan': r.no_ketetapan or '',
                    'ntpp': r.ntpp or '',
                    'jumlah': r.jumlah,
                    'tanggal': r.tanggal.strftime('%Y-%m-%d') if r.tanggal else '',
                    'tanda_tangan': r.tanda_tangan or '',
                    'keterangan': r.keterangan or '',
                    'ssp_pemungut': r.ssp_pemungut,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/ssp/create', type='json', auth='user', methods=['POST'], cors='*')
    def create_ssp(self, **kw):
        try:
            params = kw
            val = {
                'kpp': params.get('kpp'),
                'nama_wp': params.get('nama_wp'),
                'npwp': params.get('npwp'),
                'alamat': params.get('alamat'),
                'kode_pos': params.get('kode_pos'),
                'tahun': params.get('tahun'),
                'bulan': params.get('bulan'),
                'kode_jenis_pajak': params.get('kode_jenis_pajak'),
                'kode_jenis_pajak_desc': params.get('kode_jenis_pajak_desc'),
                'kode_jenis_setoran': params.get('kode_jenis_setoran'),
                'kode_jenis_setoran_desc': params.get('kode_jenis_setoran_desc'),
                'uraian_pembayaran': params.get('uraian_pembayaran'),
                'no_ketetapan': params.get('no_ketetapan'),
                'ntpp': params.get('ntpp'),
                'jumlah': params.get('jumlah', 0),
                'tanggal': params.get('tanggal') or False,
                'tanda_tangan': params.get('tanda_tangan'),
                'keterangan': params.get('keterangan'),
                'ssp_pemungut': params.get('ssp_pemungut', False),
            }
            
            if params.get('id'):
                record = request.env['invoicingbackend.surat_setoran_pajak'].browse(params['id'])
                record.write(val)
                res_id = record.id
            else:
                val['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.surat_setoran_pajak'].create(val)
                res_id = record.id
                
            return {'status': 'success', 'id': res_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/ssp/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_ssp(self, **kw):
        try:
            record_id = kw.get('id')
            if record_id:
                request.env['invoicingbackend.surat_setoran_pajak'].browse(record_id).unlink()
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
