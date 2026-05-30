from odoo import http
from odoo.http import request

class ApiSetupTandaTangan(http.Controller):
    
    @http.route('/api/setup/tandatangan/get', type='json', auth='public', methods=['POST'], cors='*')
    def get_tanda_tangan(self, **kw):
        try:
            records = request.env['invoicingbackend.tanda_tangan'].sudo().search([])
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'jenis_formulir': rec.jenis_formulir or '',
                    'nama': rec.nama or '',
                    'jabatan': rec.jabatan or '',
                    'lokasi': rec.lokasi or '',
                    'ttd_image': rec.ttd_image.decode('utf-8') if rec.ttd_image else None,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/tandatangan/save', type='json', auth='public', methods=['POST'], cors='*')
    def save_tanda_tangan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'jenis_formulir': params.get('jenis_formulir'),
                'nama': params.get('nama'),
                'jabatan': params.get('jabatan'),
                'lokasi': params.get('lokasi'),
            }
            
            # Handle base64 image
            if 'ttd_image' in params:
                ttd_str = params.get('ttd_image')
                if ttd_str and ',' in ttd_str:
                    # Strip the data:image/png;base64, prefix if present
                    ttd_str = ttd_str.split(',')[1]
                vals['ttd_image'] = ttd_str
            
            if record_id:
                record = request.env['invoicingbackend.tanda_tangan'].sudo().browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.tanda_tangan'].sudo().create(vals)
                
            return {'status': 'success', 'message': 'Tanda Tangan berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/tandatangan/delete', type='json', auth='public', methods=['POST'], cors='*')
    def delete_tanda_tangan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.tanda_tangan'].sudo().browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Tanda Tangan berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
