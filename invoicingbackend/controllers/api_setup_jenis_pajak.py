from odoo import http
from odoo.http import request

class ApiSetupJenisPajak(http.Controller):
    
    @http.route('/api/setup/jenis_pajak/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_jenis_pajak(self, **kw):
        try:
            records = request.env['invoicingbackend.jenis_pajak'].search([], order='kode asc')
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

    @http.route('/api/setup/jenis_pajak/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_jenis_pajak(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.jenis_pajak'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.jenis_pajak'].create(vals)
                
            return {'status': 'success', 'message': 'Kode Jenis Pajak berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/jenis_pajak/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_jenis_pajak(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.jenis_pajak'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Kode Jenis Pajak berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
