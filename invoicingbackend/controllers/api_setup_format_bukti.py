from odoo import http
from odoo.http import request

class ApiSetupFormatBukti(http.Controller):
    
    @http.route('/api/setup/format_bukti/get', type='json', auth='public', methods=['POST'], cors='*')
    def get_format_bukti(self, **kw):
        try:
            records = request.env['invoicingbackend.format_bukti'].sudo().search([], order='periode desc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'periode': rec.periode or '',
                    
                    'inv_vat_prefiks': rec.inv_vat_prefiks or '',
                    'inv_vat_digit': rec.inv_vat_digit or '3',
                    'inv_vat_sufiks': rec.inv_vat_sufiks or '',
                    
                    'inv_non_vat_prefiks': rec.inv_non_vat_prefiks or '',
                    'inv_non_vat_digit': rec.inv_non_vat_digit or '3',
                    'inv_non_vat_sufiks': rec.inv_non_vat_sufiks or '',
                    
                    'kwi_vat_prefiks': rec.kwi_vat_prefiks or '',
                    'kwi_vat_digit': rec.kwi_vat_digit or '3',
                    'kwi_vat_sufiks': rec.kwi_vat_sufiks or '',
                    
                    'kwi_non_vat_prefiks': rec.kwi_non_vat_prefiks or '',
                    'kwi_non_vat_digit': rec.kwi_non_vat_digit or '3',
                    'kwi_non_vat_sufiks': rec.kwi_non_vat_sufiks or '',
                    
                    'pem_inv_prefiks': rec.pem_inv_prefiks or '',
                    'pem_inv_digit': rec.pem_inv_digit or '3',
                    'pem_inv_sufiks': rec.pem_inv_sufiks or '',
                    
                    'nota_kredit_prefiks': rec.nota_kredit_prefiks or '',
                    'nota_kredit_digit': rec.nota_kredit_digit or '3',
                    'nota_kredit_sufiks': rec.nota_kredit_sufiks or '',
                    
                    'so_prefiks': rec.so_prefiks or '',
                    'so_digit': rec.so_digit or '3',
                    'so_sufiks': rec.so_sufiks or '',
                    
                    'sj_prefiks': rec.sj_prefiks or '',
                    'sj_digit': rec.sj_digit or '3',
                    'sj_sufiks': rec.sj_sufiks or '',
                    
                    'retur_jual_prefiks': rec.retur_jual_prefiks or '',
                    'retur_jual_digit': rec.retur_jual_digit or '3',
                    'retur_jual_sufiks': rec.retur_jual_sufiks or '',
                    
                    'retur_beli_prefiks': rec.retur_beli_prefiks or '',
                    'retur_beli_digit': rec.retur_beli_digit or '3',
                    'retur_beli_sufiks': rec.retur_beli_sufiks or '',
                    
                    'terima_brg_prefiks': rec.terima_brg_prefiks or '',
                    'terima_brg_digit': rec.terima_brg_digit or '3',
                    'terima_brg_sufiks': rec.terima_brg_sufiks or '',
                    
                    'adj_inv_prefiks': rec.adj_inv_prefiks or '',
                    'adj_inv_digit': rec.adj_inv_digit or '3',
                    'adj_inv_sufiks': rec.adj_inv_sufiks or '',
                    
                    'tf_brg_prefiks': rec.tf_brg_prefiks or '',
                    'tf_brg_digit': rec.tf_brg_digit or '3',
                    'tf_brg_sufiks': rec.tf_brg_sufiks or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/format_bukti/save', type='json', auth='public', methods=['POST'], cors='*')
    def save_format_bukti(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            # Remove id from params before write/create
            vals = {k: v for k, v in params.items() if k != 'id'}
            
            if record_id:
                record = request.env['invoicingbackend.format_bukti'].sudo().browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.format_bukti'].sudo().create(vals)
                
            return {'status': 'success', 'message': 'Format No Bukti berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/format_bukti/delete', type='json', auth='public', methods=['POST'], cors='*')
    def delete_format_bukti(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.format_bukti'].sudo().browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Format No Bukti berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
