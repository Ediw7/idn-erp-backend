from odoo import http
from odoo.http import request

class ApiSetupSalesman(http.Controller):
    
    @http.route('/api/setup/salesman/get', type='json', auth='public', methods=['POST'], cors='*')
    def get_salesman(self, **kw):
        try:
            records = request.env['invoicingbackend.salesman'].sudo().search([], order='kode asc')
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

    @http.route('/api/setup/salesman/save', type='json', auth='public', methods=['POST'], cors='*')
    def save_salesman(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.salesman'].sudo().browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.salesman'].sudo().create(vals)
                
            return {'status': 'success', 'message': 'Salesman berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/salesman/delete', type='json', auth='public', methods=['POST'], cors='*')
    def delete_salesman(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.salesman'].sudo().browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Salesman berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
