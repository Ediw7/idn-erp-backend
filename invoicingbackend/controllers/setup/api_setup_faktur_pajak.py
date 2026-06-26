from odoo import http
from odoo.http import request

class ApiSetupFakturPajak(http.Controller):
    
    @http.route('/api/setup/faktur_pajak/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_faktur_pajak(self, **kw):
        try:
            records = request.env['invoicingbackend.faktur_pajak'].search([], order='tgl_awal desc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_surat': rec.no_surat or '',
                    'tgl_surat': str(rec.tgl_surat) if rec.tgl_surat else '',
                    'tgl_awal': str(rec.tgl_awal) if rec.tgl_awal else '',
                    'tgl_akhir': str(rec.tgl_akhir) if rec.tgl_akhir else '',
                    'no_seri_awal': rec.no_seri_awal or '',
                    'no_seri_akhir': rec.no_seri_akhir or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/faktur_pajak/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_faktur_pajak(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'no_surat': params.get('no_surat'),
                'tgl_surat': params.get('tgl_surat') or False,
                'tgl_awal': params.get('tgl_awal') or False,
                'tgl_akhir': params.get('tgl_akhir') or False,
                'no_seri_awal': params.get('no_seri_awal'),
                'no_seri_akhir': params.get('no_seri_akhir'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.faktur_pajak'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.faktur_pajak'].create(vals)
                
            return {'status': 'success', 'message': 'Setup Faktur Pajak berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/faktur_pajak/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_faktur_pajak(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.faktur_pajak'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Setup Faktur Pajak berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
