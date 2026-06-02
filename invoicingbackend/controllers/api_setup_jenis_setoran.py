from odoo import http
from odoo.http import request

class ApiSetupJenisSetoran(http.Controller):
    
    @http.route('/api/setup/jenis_setoran/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_jenis_setoran(self, **kw):
        try:
            records = request.env['invoicingbackend.jenis_setoran'].search([], order='jenis_pajak_id asc, kode asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'jenis_pajak_id': rec.jenis_pajak_id.id if rec.jenis_pajak_id else None,
                    'jenis_pajak_kode': rec.jenis_pajak_id.kode if rec.jenis_pajak_id else '',
                    'jenis_pajak_nama': rec.jenis_pajak_id.nama if rec.jenis_pajak_id else '',
                    'kode': rec.kode or '',
                    'nama': rec.nama or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/jenis_setoran/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_jenis_setoran(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'jenis_pajak_id': params.get('jenis_pajak_id'),
                'kode': params.get('kode'),
                'nama': params.get('nama'),
            }
            
            if not vals['jenis_pajak_id']:
                return {'status': 'error', 'message': 'MAP (Jenis Pajak) harus diisi'}
                
            if record_id:
                record = request.env['invoicingbackend.jenis_setoran'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.jenis_setoran'].create(vals)
                
            return {'status': 'success', 'message': 'Kode Jenis Setoran berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/jenis_setoran/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_jenis_setoran(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.jenis_setoran'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Kode Jenis Setoran berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
