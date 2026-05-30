from odoo import http
from odoo.http import request

class ApiSetupMataUang(http.Controller):
    
    @http.route('/api/setup/matauang/get', type='json', auth='public', methods=['POST'], cors='*')
    def get_mata_uang(self, **kw):
        try:
            records = request.env['invoicingbackend.mata_uang'].sudo().search([])
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'kode': rec.kode or '',
                    'nama': rec.nama or '',
                    'per': rec.per or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/matauang/save', type='json', auth='public', methods=['POST'], cors='*')
    def save_mata_uang(self, **kw):
        try:
            params = kw
            mata_uang_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
                'per': params.get('per'),
            }
            
            if mata_uang_id:
                record = request.env['invoicingbackend.mata_uang'].sudo().browse(mata_uang_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.mata_uang'].sudo().create(vals)
                
            return {'status': 'success', 'message': 'Mata Uang berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/matauang/delete', type='json', auth='public', methods=['POST'], cors='*')
    def delete_mata_uang(self, **kw):
        try:
            params = kw
            mata_uang_id = params.get('id')
            
            if mata_uang_id:
                record = request.env['invoicingbackend.mata_uang'].sudo().browse(mata_uang_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Mata Uang berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
