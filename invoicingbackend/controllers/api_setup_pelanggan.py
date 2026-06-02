from odoo import http
from odoo.http import request

class ApiSetupPelanggan(http.Controller):
    
    @http.route('/api/setup/pelanggan/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_pelanggan(self, **kw):
        try:
            records = request.env['invoicingbackend.pelanggan'].search([], order='kode asc')
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'kode': rec.kode or '',
                    'nama': rec.nama or '',
                    'alamat': rec.alamat or '',
                    'telepon': rec.telepon or '',
                    'fax': rec.fax or '',
                    'alamat_kirim': rec.alamat_kirim or '',
                    'telepon_kirim': rec.telepon_kirim or '',
                    'fax_kirim': rec.fax_kirim or '',
                    'nama_wp': rec.nama_wp or '',
                    'npwp': rec.npwp or '',
                    'nik': rec.nik or '',
                    'alamat_wp': rec.alamat_wp or '',
                    'jenis_transaksi': rec.jenis_transaksi or '01',
                    'email': rec.email or '',
                    'contact_person': rec.contact_person or '',
                    'no_hp': rec.no_hp or '',
                    'jabatan': rec.jabatan or '',
                    'pembayaran_id': rec.pembayaran_id.id if rec.pembayaran_id else None,
                    'pembayaran_nama': rec.pembayaran_id.nama if rec.pembayaran_id else '',
                    'tingkat_harga': rec.tingkat_harga or '1',
                    'diskon': rec.diskon or 0.0,
                    'perk_piutang_id': rec.perk_piutang_id.id if rec.perk_piutang_id else None,
                    'perk_piutang_nama': rec.perk_piutang_id.no_perkiraan if rec.perk_piutang_id else '',
                    'keterangan': rec.keterangan or '',
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/pelanggan/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_pelanggan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            vals = {
                'kode': params.get('kode'),
                'nama': params.get('nama'),
                'alamat': params.get('alamat'),
                'telepon': params.get('telepon'),
                'fax': params.get('fax'),
                'alamat_kirim': params.get('alamat_kirim'),
                'telepon_kirim': params.get('telepon_kirim'),
                'fax_kirim': params.get('fax_kirim'),
                'nama_wp': params.get('nama_wp'),
                'npwp': params.get('npwp'),
                'nik': params.get('nik'),
                'alamat_wp': params.get('alamat_wp'),
                'jenis_transaksi': params.get('jenis_transaksi') or '01',
                'email': params.get('email'),
                'contact_person': params.get('contact_person'),
                'no_hp': params.get('no_hp'),
                'jabatan': params.get('jabatan'),
                'pembayaran_id': params.get('pembayaran_id') or False,
                'tingkat_harga': params.get('tingkat_harga') or '1',
                'diskon': float(params.get('diskon', 0.0)),
                'perk_piutang_id': params.get('perk_piutang_id') or False,
                'keterangan': params.get('keterangan'),
            }
            
            if record_id:
                record = request.env['invoicingbackend.pelanggan'].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                record = request.env['invoicingbackend.pelanggan'].create(vals)
                
            return {'status': 'success', 'message': 'Pelanggan berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/pelanggan/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_pelanggan(self, **kw):
        try:
            params = kw
            record_id = params.get('id')
            
            if record_id:
                record = request.env['invoicingbackend.pelanggan'].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {'status': 'success', 'message': 'Pelanggan berhasil dihapus'}
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            return {'status': 'error', 'message': 'ID tidak valid'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/pelanggan/import_batch', type='json', auth='user', methods=['POST'], cors='*')
    def import_batch_pelanggan(self, **kw):
        try:
            params = kw
            items = params.get('items', [])
            if not items:
                return {'status': 'error', 'message': 'Data kosong'}
                
            env_pelanggan = request.env['invoicingbackend.pelanggan']
            success_count = 0
            
            for item in items:
                if not item.get('kode') or not item.get('nama'):
                    continue
                    
                # Check if exists by kode
                existing = env_pelanggan.search([('kode', '=', item.get('kode'))], limit=1)
                
                vals = {
                    'kode': item.get('kode'),
                    'nama': item.get('nama'),
                    'alamat': item.get('alamat'),
                    'telepon': item.get('telepon'),
                    'fax': item.get('fax'),
                    'alamat_kirim': item.get('alamat_kirim'),
                    'telepon_kirim': item.get('telepon_kirim'),
                    'fax_kirim': item.get('fax_kirim'),
                    'nama_wp': item.get('nama_wp'),
                    'npwp': item.get('npwp'),
                    'alamat_wp': item.get('alamat_wp'),
                }
                
                if existing:
                    existing.write(vals)
                else:
                    env_pelanggan.create(vals)
                success_count += 1
                
            return {'status': 'success', 'message': f'Berhasil mengimpor {success_count} data pelanggan'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
