from odoo import http
from odoo.http import request

class ApiSetupBahasa(http.Controller):
    
    @http.route('/api/setup/bahasa/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_bahasa(self, **kw):
        try:
            records = request.env['invoicingbackend.bahasa'].search([], order='jenis_objek asc, nama_objek asc, id asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'jenis_objek': rec.jenis_objek or '',
                    'nama_objek': rec.nama_objek or '',
                    'default_sistem': rec.default_sistem or '',
                    'judul_kustom': rec.judul_kustom or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/bahasa/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_bahasa(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'jenis_objek': params.get('jenis_objek'),
                'nama_objek': params.get('nama_objek'),
                'default_sistem': params.get('default_sistem'),
                'judul_kustom': params.get('judul_kustom') or '',
            }
            
            if record_id:
                record = request.env['invoicingbackend.bahasa'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.bahasa'].create(vals)
                
            return {'status': 'success', 'message': 'Setup Bahasa berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/bahasa/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_bahasa(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.bahasa'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Setup Bahasa berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
