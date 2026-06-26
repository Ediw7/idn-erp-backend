from odoo import http
from odoo.http import request

class ApiSetupGudang(http.Controller):
    
    @http.route('/api/setup/gudang/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_gudang(self, **kw):
        try:
            records = request.env['invoicingbackend.gudang'].search([], order='kode_gudang asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'kode_gudang': rec.kode_gudang,
                    'nama_gudang': rec.nama_gudang,
                    'lokasi': rec.lokasi or '',
                    'is_default': rec.is_default,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/gudang/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_gudang(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            is_default = bool(params.get('is_default', False))
            
            vals = {
                'kode_gudang': params.get('kode_gudang'),
                'nama_gudang': params.get('nama_gudang'),
                'lokasi': params.get('lokasi'),
                'is_default': is_default,
            }
            
            # Uncheck other defaults if this one is set to default
            if is_default:
                other_defaults = request.env['invoicingbackend.gudang'].search([('is_default', '=', True)])
                if record_id:
                    other_defaults = other_defaults.filtered(lambda r: r.id != record_id)
                other_defaults.write({'is_default': False})
            
            if record_id:
                record = request.env['invoicingbackend.gudang'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.gudang'].create(vals)
                
            return {'status': 'success', 'message': 'Data Gudang berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/gudang/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_gudang(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.gudang'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Gudang berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
