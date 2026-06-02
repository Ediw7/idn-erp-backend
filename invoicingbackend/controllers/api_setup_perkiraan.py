from odoo import http
from odoo.http import request

class ApiSetupPerkiraan(http.Controller):
    
    @http.route('/api/setup/perkiraan/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_perkiraan(self, **kw):
        try:
            params = kw
            domain = []
            
            no_perkiraan = params.get('no_perkiraan')
            if no_perkiraan:
                domain.append(('no_perkiraan', 'ilike', no_perkiraan))
                
            nama_perkiraan = params.get('nama_perkiraan')
            if nama_perkiraan:
                domain.append(('nama_perkiraan', 'ilike', nama_perkiraan))
                
            records = request.env['invoicingbackend.perkiraan'].search(domain, order='no_perkiraan asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_perkiraan': rec.no_perkiraan,
                    'nama_perkiraan': rec.nama_perkiraan,
                    'kas_bank': rec.kas_bank,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/perkiraan/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_perkiraan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'no_perkiraan': params.get('no_perkiraan'),
                'nama_perkiraan': params.get('nama_perkiraan'),
                'kas_bank': bool(params.get('kas_bank', False)),
            }
            
            if record_id:
                record = request.env['invoicingbackend.perkiraan'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.perkiraan'].create(vals)
                
            return {'status': 'success', 'message': 'Perkiraan berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/perkiraan/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_perkiraan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.perkiraan'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Perkiraan berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
