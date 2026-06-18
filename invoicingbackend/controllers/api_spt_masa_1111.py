from odoo import http
from odoo.http import request

class ApiSptMasa1111(http.Controller):

    @http.route('/api/spt-masa/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_spt_masa(self, **kw):
        try:
            records = request.env['invoicingbackend.spt_masa_1111'].search([])
            data = []
            for r in records:
                data.append({
                    'id': r.id,
                    'tahun': r.tahun,
                    'masa_awal': r.masa_awal,
                    'masa_akhir': r.masa_akhir,
                    'pembetulan_ke': r.pembetulan_ke,
                    'tanggal_spt': r.tanggal_spt.strftime('%Y-%m-%d') if r.tanggal_spt else '',
                    'is_locked': r.is_locked,
                    'dpp_ekspor': r.dpp_ekspor,
                    'ppn_ekspor': r.ppn_ekspor,
                    'dpp_dipungut_sendiri': r.dpp_dipungut_sendiri,
                    'ppn_dipungut_sendiri': r.ppn_dipungut_sendiri,
                    'dpp_dipungut_pemungut': r.dpp_dipungut_pemungut,
                    'ppn_dipungut_pemungut': r.ppn_dipungut_pemungut,
                    'dpp_tidak_dipungut': r.dpp_tidak_dipungut,
                    'ppn_tidak_dipungut': r.ppn_tidak_dipungut,
                    'dpp_dibebaskan': r.dpp_dibebaskan,
                    'ppn_dibebaskan': r.ppn_dibebaskan,
                    'dpp_tidak_terutang': r.dpp_tidak_terutang,
                    'ppn_disetor_dimuka': r.ppn_disetor_dimuka,
                    'pajak_masukan_diperhitungkan': r.pajak_masukan_diperhitungkan,
                    'ppn_spt_dibetulkan': r.ppn_spt_dibetulkan,
                    'tgl_lunas_kurang_bayar': r.tgl_lunas_kurang_bayar.strftime('%Y-%m-%d') if r.tgl_lunas_kurang_bayar else '',
                    'ntpn_kurang_bayar': r.ntpn_kurang_bayar or '',
                    'lebih_bayar_pada': r.lebih_bayar_pada or '',
                    'lebih_bayar_oleh': r.lebih_bayar_oleh or '',
                    'lebih_bayar_diminta_untuk': r.lebih_bayar_diminta_untuk or '',
                    'kompensasi_masa': r.kompensasi_masa or '',
                    'kompensasi_tahun': r.kompensasi_tahun or '',
                    'restitusi_pasal_17c': r.restitusi_pasal_17c or '',
                    'restitusi_pasal_17d': r.restitusi_pasal_17d or '',
                    'restitusi_pasal_9_4c': r.restitusi_pasal_9_4c,
                    'membangun_dpp': r.membangun_dpp,
                    'membangun_ppn': r.membangun_ppn
                })
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/spt-masa/create', type='json', auth='user', methods=['POST'], cors='*')
    def create_spt_masa(self, **kw):
        try:
            params = kw
            val = {
                'tahun': params.get('tahun'),
                'masa_awal': params.get('masa_awal'),
                'masa_akhir': params.get('masa_akhir'),
                'pembetulan_ke': params.get('pembetulan_ke'),
                'tanggal_spt': params.get('tanggal_spt') or False,
                'is_locked': params.get('is_locked', False),
                'dpp_ekspor': params.get('dpp_ekspor', 0),
                'ppn_ekspor': params.get('ppn_ekspor', 0),
                'dpp_dipungut_sendiri': params.get('dpp_dipungut_sendiri', 0),
                'ppn_dipungut_sendiri': params.get('ppn_dipungut_sendiri', 0),
                'dpp_dipungut_pemungut': params.get('dpp_dipungut_pemungut', 0),
                'ppn_dipungut_pemungut': params.get('ppn_dipungut_pemungut', 0),
                'dpp_tidak_dipungut': params.get('dpp_tidak_dipungut', 0),
                'ppn_tidak_dipungut': params.get('ppn_tidak_dipungut', 0),
                'dpp_dibebaskan': params.get('dpp_dibebaskan', 0),
                'ppn_dibebaskan': params.get('ppn_dibebaskan', 0),
                'dpp_tidak_terutang': params.get('dpp_tidak_terutang', 0),
                'ppn_disetor_dimuka': params.get('ppn_disetor_dimuka', 0),
                'pajak_masukan_diperhitungkan': params.get('pajak_masukan_diperhitungkan', 0),
                'ppn_spt_dibetulkan': params.get('ppn_spt_dibetulkan', 0),
                'tgl_lunas_kurang_bayar': params.get('tgl_lunas_kurang_bayar') or False,
                'ntpn_kurang_bayar': params.get('ntpn_kurang_bayar'),
                'lebih_bayar_pada': params.get('lebih_bayar_pada') or False,
                'lebih_bayar_oleh': params.get('lebih_bayar_oleh') or False,
                'lebih_bayar_diminta_untuk': params.get('lebih_bayar_diminta_untuk') or False,
                'kompensasi_masa': params.get('kompensasi_masa') or False,
                'kompensasi_tahun': params.get('kompensasi_tahun'),
                'restitusi_pasal_17c': params.get('restitusi_pasal_17c') or False,
                'restitusi_pasal_17d': params.get('restitusi_pasal_17d') or False,
                'restitusi_pasal_9_4c': params.get('restitusi_pasal_9_4c', False),
                'membangun_dpp': params.get('membangun_dpp', 0),
                'membangun_ppn': params.get('membangun_ppn', 0)
            }
            
            if params.get('id'):
                record = request.env['invoicingbackend.spt_masa_1111'].browse(params['id'])
                record.write(val)
                res_id = record.id
            else:
                val['company_id'] = request.env.user.company_id.id
                record = request.env['invoicingbackend.spt_masa_1111'].create(val)
                res_id = record.id
                
            return {'status': 'success', 'id': res_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/spt-masa/delete', type='json', auth='user', methods=['POST'], cors='*')
    def delete_spt_masa(self, **kw):
        try:
            record_id = kw.get('id')
            if record_id:
                request.env['invoicingbackend.spt_masa_1111'].browse(record_id).unlink()
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
