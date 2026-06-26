from odoo import http
from odoo.http import request

class ApiSetupGroupBarang(http.Controller):
    
    @http.route('/api/setup/groupbarang/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_group_barang(self, **kw):
        try:
            records = request.env['invoicingbackend.group_barang'].search([], order='nama asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'nama': rec.nama,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/groupbarang/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_group_barang(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'nama': params.get('nama'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.group_barang'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.group_barang'].create(vals)
                
            return {'status': 'success', 'message': 'Group Barang berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/groupbarang/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_group_barang(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.group_barang'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Group Barang berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
