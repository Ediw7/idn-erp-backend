from odoo import http
from odoo.http import request
from datetime import datetime


class ApiSalesOrder(http.Controller):

    @http.route('/api/sales-order/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_sales_order(self, **kw):
        try:
            params = kw
            domain = []

            if params.get('no_so'):
                domain.append(('no_so', 'ilike', params['no_so']))
            if params.get('pelanggan_id'):
                domain.append(('pelanggan_id', '=', int(params['pelanggan_id'])))
            if params.get('periode'):
                # periode format: YYYYMM
                yr = int(str(params['periode'])[:4])
                mn = int(str(params['periode'])[4:6])
                domain.append(('tgl_so', '>=', f'{yr}-{mn:02d}-01'))
                import calendar
                last_day = calendar.monthrange(yr, mn)[1]
                domain.append(('tgl_so', '<=', f'{yr}-{mn:02d}-{last_day:02d}'))

            limit = int(params.get('limit', 2000))
            records = request.env['invoicingbackend.sales_order'].search(domain, order='tgl_so desc, no_so desc', limit=limit)
            data = []
            for rec in records:
                lines = []
                for line in rec.line_ids:
                    lines.append({
                        'id': line.id,
                        'item_id': line.item_id.id if line.item_id else None,
                        'kode_barang': line.item_id.kode if line.item_id else '',
                        'nama_barang': line.nama_barang or '',
                        'satuan': line.satuan or '',
                        'kuantum': line.kuantum,
                        'harga_satuan': line.harga_satuan,
                        'disc_persen': line.disc_persen,
                        'disc_harga': line.disc_harga,
                        'harga_jual': line.harga_jual,
                        'keterangan': line.keterangan or '',
                    })
                data.append({
                    'id': rec.id,
                    'no_so': rec.no_so or '',
                    'tgl_so': rec.tgl_so.strftime('%Y-%m-%d') if rec.tgl_so else '',
                    'pelanggan_id': rec.pelanggan_id.id if rec.pelanggan_id else None,
                    'pelanggan_nama': rec.pelanggan_id.nama if rec.pelanggan_id else '',
                    'pelanggan_alamat_kirim': rec.pelanggan_id.alamat_kirim if rec.pelanggan_id else '',
                    'alamat_kirim': rec.alamat_kirim or '',
                    'no_po': rec.no_po or '',
                    'tgl_po': rec.tgl_po.strftime('%Y-%m-%d') if rec.tgl_po else '',
                    'mata_uang_id': rec.mata_uang_id.id if rec.mata_uang_id else None,
                    'mata_uang_kode': rec.mata_uang_id.kode if rec.mata_uang_id else '',
                    'pembayaran_id': rec.pembayaran_id.id if rec.pembayaran_id else None,
                    'pembayaran_nama': rec.pembayaran_id.nama if rec.pembayaran_id else '',
                    'salesman_id': rec.salesman_id.id if rec.salesman_id else None,
                    'salesman_nama': rec.salesman_id.nama if rec.salesman_id else '',
                    'tgl_kirim': rec.tgl_kirim.strftime('%Y-%m-%d') if rec.tgl_kirim else '',
                    'dipesan_oleh': rec.dipesan_oleh or '',
                    'is_closed': rec.is_closed,
                    'is_void': rec.is_void,
                    'keterangan': rec.keterangan or '',
                    'subtotal': rec.subtotal,
                    'potongan_harga': rec.potongan_harga,
                    'ppn_persen': rec.ppn_persen,
                    'ppn_amount': rec.ppn_amount,
                    'ppnbm_persen': rec.ppnbm_persen,
                    'ppnbm_amount': rec.ppnbm_amount,
                    'ongkos_angkut': rec.ongkos_angkut,
                    'total': rec.total,
                    'create_date': rec.create_date.strftime('%m/%d/%Y %I:%M:%S %p') if rec.create_date else '',
                    'create_uid_name': rec.create_uid.name if rec.create_uid else '',
                    'write_date': rec.write_date.strftime('%m/%d/%Y %I:%M:%S %p') if rec.write_date else '',
                    'write_uid_name': rec.write_uid.name if rec.write_uid else '',
                    'lines': lines,
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/sales-order/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_sales_order(self, **kw):
        try:
            params = kw
            record_id = params.get('id')

            vals = {
                'no_so': params.get('no_so', ''),
                'tgl_so': params.get('tgl_so') or False,
                'pelanggan_id': int(params['pelanggan_id']) if params.get('pelanggan_id') else False,
                'alamat_kirim': params.get('alamat_kirim', ''),
                'no_po': params.get('no_po', ''),
                'tgl_po': params.get('tgl_po') or False,
                'mata_uang_id': int(params['mata_uang_id']) if params.get('mata_uang_id') else False,
                'pembayaran_id': int(params['pembayaran_id']) if params.get('pembayaran_id') else False,
                'salesman_id': int(params['salesman_id']) if params.get('salesman_id') else False,
                'tgl_kirim': params.get('tgl_kirim') or False,
                'dipesan_oleh': params.get('dipesan_oleh', ''),
                'is_closed': params.get('is_closed', False),
                'is_void': params.get('is_void', False),
                'keterangan': params.get('keterangan', ''),
                'potongan_harga': float(params.get('potongan_harga', 0)),
                'ppn_persen': float(params.get('ppn_persen', 10.0)),
                'ppnbm_persen': float(params.get('ppnbm_persen', 0.0)),
                'ongkos_angkut': float(params.get('ongkos_angkut', 0)),
            }

            lines_data = params.get('lines', [])
            line_commands = [(5, 0, 0)]  # First clear all lines
            for line in lines_data:
                line_vals = {
                    'item_id': int(line['item_id']) if line.get('item_id') else False,
                    'satuan': line.get('satuan', ''),
                    'kuantum': float(line.get('kuantum', 1)),
                    'harga_satuan': float(line.get('harga_satuan', 0)),
                    'disc_persen': float(line.get('disc_persen', 0)),
                    'disc_harga': float(line.get('disc_harga', 0)),
                    'keterangan': line.get('keterangan', ''),
                }
                line_commands.append((0, 0, line_vals))

            vals['line_ids'] = line_commands

            if record_id:
                record = request.env['invoicingbackend.sales_order'].browse(int(record_id))
                if record.exists():
                    record.write(vals)
                else:
                    return {'status': 'error', 'message': 'Data tidak ditemukan'}
            else:
                vals['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.sales_order'].create(vals)

            return {'status': 'success', 'message': 'Sales Order berhasil disimpan', 'id': record.id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/sales-order/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_sales_order(self, **kw):
        try:
            record_id = kw.get('id')
            if not record_id:
                return {'status': 'error', 'message': 'ID tidak valid'}
            record = request.env['invoicingbackend.sales_order'].browse(int(record_id))
            if record.exists():
                record.unlink()
                return {'status': 'success', 'message': 'Sales Order berhasil dihapus'}
            return {'status': 'error', 'message': 'Data tidak ditemukan'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/sales-order/auto-no', type='json', auth='user', methods=['POST'], cors='*')
    def auto_no_so(self, **kw):
        try:
            from datetime import date
            today = date.today()
            month_str = f'{today.month:02d}'
            year_str = str(today.year)
            # Find the latest SO for this month/year
            prefix = f'SO/'
            records = request.env['invoicingbackend.sales_order'].search(
                [('no_so', 'like', f'SO/%/{month_str}/{year_str}')],
                order='no_so desc', limit=1
            )
            if records:
                last_no = records[0].no_so
                parts = last_no.split('/')
                try:
                    seq = int(parts[1]) + 1
                except:
                    seq = 1
            else:
                seq = 1
            new_no = f'SO/{seq:03d}/{month_str}/{year_str}'
            return {'status': 'success', 'no_so': new_no}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
