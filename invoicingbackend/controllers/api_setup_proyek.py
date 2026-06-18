from odoo import http
from odoo.http import request

class ApiSetupProyek(http.Controller):
    
    @http.route('/api/setup/proyek/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_proyek(self, **kw):
        try:
            records = request.env['invoicingbackend.proyek'].search([], order='kode asc')
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

    @http.route('/api/setup/proyek/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_proyek(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.proyek'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.proyek'].create(vals)
                
            return {'status': 'success', 'message': 'Proyek berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/proyek/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_proyek(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.proyek'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Proyek berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
