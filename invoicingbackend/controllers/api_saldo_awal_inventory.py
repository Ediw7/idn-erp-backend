from odoo import http
from odoo.http import request
import json

class ApiSaldoAwalInventory(http.Controller):

    @http.route('/api/inventory/saldo-awal/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_saldo_awal(self, **kw):
        try:
            records = request.env['invoicingbackend.saldo_awal_inventory'].search([], order='tanggal desc, id desc')
            data = []
            for rec in records:
                lines = []
                for line in rec.line_ids:
                    lines.append({
                        'id': line.id,
                        'item_id': line.item_id.id if line.item_id else None,
                        'item_kode': line.item_id.kode if line.item_id else '',
                        'item_nama': line.item_id.nama if line.item_id else '',
                        'satuan': line.item_id.satuan if line.item_id else '',
                        'quantity': line.quantity,
                        'hpp': line.hpp
                    })
                data.append({
                    'id': rec.id,
                    'gudang_id': rec.gudang_id.id if rec.gudang_id else None,
                    'gudang_nama': rec.gudang_id.nama_gudang if rec.gudang_id else '',
                    'tanggal': str(rec.tanggal) if rec.tanggal else '',
                    'keterangan': rec.keterangan or '',
                    'lines': lines
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/inventory/saldo-awal/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_saldo_awal(self, **kw):
        try:
            params = request.jsonrequest
            record_id = params.get('id')
            
            lines_data = []
            if 'lines' in params:
                for line in params['lines']:
                    line_vals = {
                        'item_id': line.get('item_id'),
                        'quantity': line.get('quantity', 0),
                        'hpp': line.get('hpp', 0),
                    }
                    if line.get('id'):
                        lines_data.append((1, line['id'], line_vals))
                    else:
                        lines_data.append((0, 0, line_vals))
            
            # Find lines to delete
            if record_id:
                existing_record = request.env['invoicingbackend.saldo_awal_inventory'].browse(record_id)
                existing_line_ids = existing_record.line_ids.ids
                incoming_line_ids = [l.get('id') for l in params.get('lines', []) if l.get('id')]
                lines_to_delete = set(existing_line_ids) - set(incoming_line_ids)
                for l_id in lines_to_delete:
                    lines_data.append((2, l_id, 0))

            vals = {
                'gudang_id': params.get('gudang_id'),
                'tanggal': params.get('tanggal'),
                'keterangan': params.get('keterangan'),
                'line_ids': lines_data
            }

            if record_id:
                record = request.env['invoicingbackend.saldo_awal_inventory'].browse(record_id)
                record.write(vals)
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.saldo_awal_inventory'].create(vals)
                
            return {'status': 'success', 'message': 'Data berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/inventory/saldo-awal/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_saldo_awal(self, **kw):
        try:
            params = request.jsonrequest
            record_id = params.get('id')
            if record_id:
                record = request.env['invoicingbackend.saldo_awal_inventory'].browse(record_id)
                record.unlink()
                return {'status': 'success', 'message': 'Data berhasil dihapus'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
