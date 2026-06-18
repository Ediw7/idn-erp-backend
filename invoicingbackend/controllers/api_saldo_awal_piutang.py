import json
from odoo import http
from odoo.http import request
from .api_response import ApiResponse

class ApiSaldoAwalPiutang(http.Controller):
    @http.route('/api/saldo-awal-piutang/get', type='http', auth='user', methods=['GET', 'POST', 'OPTIONS'], csrf=False, cors='*')
    def get_saldo_awal_piutang(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            records = request.env['invoicingbackend.saldo_awal_piutang'].search([])
            data = []
            for rec in records:
                data.append({
                    'id': rec.id,
                    'no_invoice': rec.no_invoice,
                    'tanggal': str(rec.tanggal) if rec.tanggal else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else False,
                    'pelanggan_name': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'alamat': rec.pelanggan_id.alamat if rec.pelanggan_id else '',
                    'proyek_id': rec.proyek_id.id if rec.proyek_id else False,
                    'proyek_name': rec.proyek_id.kode if rec.proyek_id else '',
                    'tgl_jt': str(rec.tgl_jt) if rec.tgl_jt else '',
                    'mata_uang_id': rec.mata_uang_id.id if rec.mata_uang_id else False,
                    'mata_uang_name': rec.mata_uang_id.kode if rec.mata_uang_id else '',
                    'saldo_invoice': rec.saldo_invoice,
                    'is_paid': rec.is_paid
                })
            return ApiResponse.success(data=data)
        except Exception as e:
            return ApiResponse.error(message=str(e))

    @http.route('/api/saldo-awal-piutang/create', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def create_saldo_awal_piutang(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data)
            
            # Validation
            if not data.get('no_invoice') or not data.get('tanggal') or not data.get('pelanggan_id'):
                return ApiResponse.error(message="No Invoice, Tanggal, dan Pelanggan harus diisi!")
                
            val = {
                'no_invoice': data.get('no_invoice'),
                'tanggal': data.get('tanggal'),
                'pelanggan_id': data.get('pelanggan_id'),
                'proyek_id': data.get('proyek_id') if data.get('proyek_id') else False,
                'tgl_jt': data.get('tgl_jt') if data.get('tgl_jt') else False,
                'mata_uang_id': data.get('mata_uang_id') if data.get('mata_uang_id') else False,
                'saldo_invoice': float(data.get('saldo_invoice', 0.0) or 0.0),
                'is_paid': data.get('is_paid', False)
            }
            val['company_id'] = request.env.user.company_id.id
            new_record = request.env['invoicingbackend.saldo_awal_piutang'].create(val)
            return ApiResponse.success(message='Data berhasil disimpan', data={'id': new_record.id})
        except Exception as e:
            return ApiResponse.error(message=str(e))

    @http.route('/api/saldo-awal-piutang/update', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def update_saldo_awal_piutang(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data)
            record_id = data.get('id')
            if not record_id:
                return ApiResponse.error(message='ID tidak valid')
                
            record = request.env['invoicingbackend.saldo_awal_piutang'].browse(record_id)
            if record.exists():
                val = {}
                if 'no_invoice' in data: val['no_invoice'] = data['no_invoice']
                if 'tanggal' in data: val['tanggal'] = data['tanggal']
                if 'pelanggan_id' in data: val['pelanggan_id'] = data['pelanggan_id']
                if 'proyek_id' in data: val['proyek_id'] = data['proyek_id'] if data['proyek_id'] else False
                if 'tgl_jt' in data: val['tgl_jt'] = data['tgl_jt'] if data['tgl_jt'] else False
                if 'mata_uang_id' in data: val['mata_uang_id'] = data['mata_uang_id'] if data['mata_uang_id'] else False
                if 'saldo_invoice' in data: val['saldo_invoice'] = float(data['saldo_invoice'] or 0.0)
                if 'is_paid' in data: val['is_paid'] = data['is_paid']
                
                record.write(val)
                return ApiResponse.success(message='Data berhasil diupdate')
            return ApiResponse.error(message='Data tidak ditemukan')
        except Exception as e:
            return ApiResponse.error(message=str(e))

    @http.route('/api/saldo-awal-piutang/delete', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def delete_saldo_awal_piutang(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data)
            record_id = data.get('id')
            if not record_id:
                return ApiResponse.error(message='ID tidak valid')
                
            record = request.env['invoicingbackend.saldo_awal_piutang'].browse(record_id)
            if record.exists():
                record.unlink()
                return ApiResponse.success(message='Data berhasil dihapus')
            return ApiResponse.error(message='Data tidak ditemukan')
        except Exception as e:
            return ApiResponse.error(message=str(e))
