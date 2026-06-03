import json
from odoo import http
from odoo.http import request

class ApiSaldoAwalPiutang(http.Controller):
    @http.route('/api/saldo-awal-piutang/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_saldo_awal_piutang(self, **kw):
        try:
            records = request.env['invoicingbackend.saldo_awal_piutang'].search([])
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_invoice': rec.no_invoice,
                    'tanggal': str(rec.tanggal) if rec.tanggal else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else False,
                    'pelanggan_name': rec.pelanggan_id.nama_pelanggan if rec.pelanggan_id else '',
                    'alamat': rec.pelanggan_id.alamat_pelanggan if rec.pelanggan_id else '',
                    'proyek_id': rec.proyek_id.id if rec.proyek_id else False,
                    'proyek_name': rec.proyek_id.kode_proyek if rec.proyek_id else '',
                    'tgl_jt': str(rec.tgl_jt) if rec.tgl_jt else '',
                    'mata_uang_id': rec.mata_uang_id.id if rec.mata_uang_id else False,
                    'mata_uang_name': rec.mata_uang_id.kode if rec.mata_uang_id else '',
                    'saldo_invoice': rec.saldo_invoice,
                    'is_paid': rec.is_paid
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/saldo-awal-piutang/create', type='json', auth='user', methods=['POST'], cors='*')
    def create_saldo_awal_piutang(self, **kw):
        data = kw
        try:
            val = {
                'no_invoice': data.get('no_invoice'),
                'tanggal': data.get('tanggal'),
                'pelanggan_id': data.get('pelanggan_id'),
                'proyek_id': data.get('proyek_id'),
                'tgl_jt': data.get('tgl_jt'),
                'mata_uang_id': data.get('mata_uang_id'),
                'saldo_invoice': data.get('saldo_invoice', 0.0),
                'is_paid': data.get('is_paid', False)
            }
            new_record = request.env['invoicingbackend.saldo_awal_piutang'].create(val)
            return {'status': 'success', 'message': 'Data berhasil disimpan', 'id': new_record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/saldo-awal-piutang/update', type='json', auth='user', methods=['POST'], cors='*')
    def update_saldo_awal_piutang(self, **kw):
        data = kw
        try:
            record_id = data.get('id')
            record = request.env['invoicingbackend.saldo_awal_piutang'].browse(record_id)
            if record.exists():
                val = {}
                if 'no_invoice' in data: val['no_invoice'] = data['no_invoice']
                if 'tanggal' in data: val['tanggal'] = data['tanggal']
                if 'pelanggan_id' in data: val['pelanggan_id'] = data['pelanggan_id']
                if 'proyek_id' in data: val['proyek_id'] = data['proyek_id']
                if 'tgl_jt' in data: val['tgl_jt'] = data['tgl_jt']
                if 'mata_uang_id' in data: val['mata_uang_id'] = data['mata_uang_id']
                if 'saldo_invoice' in data: val['saldo_invoice'] = data['saldo_invoice']
                if 'is_paid' in data: val['is_paid'] = data['is_paid']
                
                record.write(val)
                return {'status': 'success', 'message': 'Data berhasil diupdate'}
            return {'status': 'error', 'message': 'Data tidak ditemukan'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/saldo-awal-piutang/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_saldo_awal_piutang(self, **kw):
        try:
            record_id = kw.get('id')
            record = request.env['invoicingbackend.saldo_awal_piutang'].browse(record_id)
            if record.exists():
                record.unlink()
                return {'status': 'success', 'message': 'Data berhasil dihapus'}
            return {'status': 'error', 'message': 'Data tidak ditemukan'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
