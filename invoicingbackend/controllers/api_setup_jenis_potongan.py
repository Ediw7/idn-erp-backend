from odoo import http
from odoo.http import request

class ApiSetupJenisPotongan(http.Controller):
    
    @http.route('/api/setup/jenis_potongan/get', type='json', auth='public', methods=['POST'], cors='*')
    def get_jenis_potongan(self, **kw):
        try:
            records = request.env['invoicingbackend.jenis_potongan'].sudo().search([], order='kode asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'kode': rec.kode or '',
                    'nama': rec.nama or '',
                    'perkiraan_id': rec.perkiraan_id.id if rec.perkiraan_id else None,
                    'perkiraan_nama': f"{rec.perkiraan_id.no_perkiraan} - {rec.perkiraan_id.nama_perkiraan}" if rec.perkiraan_id else '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/jenis_potongan/save', type='json', auth='public', methods=['POST'], cors='*')
    def save_jenis_potongan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
                'perkiraan_id': params.get('perkiraan_id') or False,
            }
            
            if record_id:
                record = request.env['invoicingbackend.jenis_potongan'].sudo().browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.jenis_potongan'].sudo().create(vals)
                
            return {'status': 'success', 'message': 'Jenis Potongan berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/jenis_potongan/delete', type='json', auth='public', methods=['POST'], cors='*')
    def delete_jenis_potongan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.jenis_potongan'].sudo().browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Jenis Potongan berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
