from odoo import http
from odoo.http import request

class ApiSetupProyek(http.Controller):
    
    @http.route('/api/setup/proyek/get', type='json', auth='public', methods=['POST'], cors='*')
    def get_proyek(self, **kw):
        try:
            records = request.env['invoicingbackend.proyek'].sudo().search([], order='kode asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'kode': rec.kode or '',
                    'nama': rec.nama or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/proyek/save', type='json', auth='public', methods=['POST'], cors='*')
    def save_proyek(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.proyek'].sudo().browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.proyek'].sudo().create(vals)
                
            return {'status': 'success', 'message': 'Proyek berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/proyek/delete', type='json', auth='public', methods=['POST'], cors='*')
    def delete_proyek(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.proyek'].sudo().browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Proyek berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
