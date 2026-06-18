from odoo import http
from odoo.http import request

class ApiSetupKursPajak(http.Controller):
    
    @http.route('/api/setup/kurspajak/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_kurs_pajak(self, **kw):
        try:
            mata_uang_id = kw.get('mata_uang_id')
            if not mata_uang_id:
                return {'status': 'error', 'message': 'ID Mata Uang wajib diisi'}
                
            records = request.env['invoicingbackend.kurs_pajak'].search([('mata_uang_id', '=', int(mata_uang_id))], order='tgl_dari desc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'mata_uang_id': rec.mata_uang_id.id,
                    'tgl_dari': str(rec.tgl_dari) if rec.tgl_dari else '',
                    'tgl_sd': str(rec.tgl_sd) if rec.tgl_sd else '',
                    'kurs': rec.kurs,
                    'no_kmk': rec.no_kmk or '',
                    'tgl_kmk': str(rec.tgl_kmk) if rec.tgl_kmk else '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/kurspajak/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_kurs_pajak(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            mata_uang_id = params.get('mata_uang_id')
            
            if not mata_uang_id:
                return {'status': 'error', 'message': 'Mata Uang wajib diisi'}
                
            vals = {
                'mata_uang_id': int(mata_uang_id),
                'tgl_dari': params.get('tgl_dari'),
                'tgl_sd': params.get('tgl_sd'),
                'kurs': float(params.get('kurs', 0)),
                'no_kmk': params.get('no_kmk'),
                'tgl_kmk': params.get('tgl_kmk') or False,
            }
            
            if record_id:
                record = request.env['invoicingbackend.kurs_pajak'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.kurs_pajak'].create(vals)
                
            return {'status': 'success', 'message': 'Kurs Pajak berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/kurspajak/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_kurs_pajak(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.kurs_pajak'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Kurs Pajak berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
