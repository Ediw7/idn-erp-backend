from odoo import http
from odoo.http import request

class ApiSetupItem(http.Controller):
    
    @http.route('/api/setup/item/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_item(self, **kw):
        try:
            params = kw
            domain = []
            
            if params.get('kode'):
                domain.append(('kode', 'ilike', params.get('kode')))
            if params.get('nama'):
                domain.append(('nama', 'ilike', params.get('nama')))
            if params.get('group_barang_id'):
                domain.append(('group_barang_id', '=', int(params.get('group_barang_id'))))
                
            records = request.env['invoicingbackend.item'].search(domain, order='kode asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'kode': rec.kode,
                    'nama': rec.nama,
                    'group_barang_id': rec.group_barang_id.id if rec.group_barang_id else None,
                    'group_barang_nama': rec.group_barang_id.nama if rec.group_barang_id else '',
                    'satuan': rec.satuan or '',
                    'harga_jual_1': rec.harga_jual_1,
                    'harga_jual_2': rec.harga_jual_2,
                    'harga_jual_3': rec.harga_jual_3,
                    'supplier_utama': rec.supplier_utama or '',
                    'perk_penjualan_id': rec.perk_penjualan_id.id if rec.perk_penjualan_id else None,
                    'perk_penjualan_nama': rec.perk_penjualan_id.no_perkiraan if rec.perk_penjualan_id else '',
                    'perk_hpp_id': rec.perk_hpp_id.id if rec.perk_hpp_id else None,
                    'perk_hpp_nama': rec.perk_hpp_id.no_perkiraan if rec.perk_hpp_id else '',
                    'is_inventory': rec.is_inventory,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/item/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_item(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
                'group_barang_id': params.get('group_barang_id') or False,
                'satuan': params.get('satuan') or 'Pcs',
                'harga_jual_1': float(params.get('harga_jual_1', 0.0)),
                'harga_jual_2': float(params.get('harga_jual_2', 0.0)),
                'harga_jual_3': float(params.get('harga_jual_3', 0.0)),
                'supplier_utama': params.get('supplier_utama'),
                'perk_penjualan_id': params.get('perk_penjualan_id') or False,
                'perk_hpp_id': params.get('perk_hpp_id') or False,
                'is_inventory': bool(params.get('is_inventory', True)),
            }
            
            if record_id:
                record = request.env['invoicingbackend.item'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.item'].create(vals)
                
            return {'status': 'success', 'message': 'Item berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/item/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_item(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.item'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Item berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
