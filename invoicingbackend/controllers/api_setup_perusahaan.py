from odoo import http
from odoo.http import request
from .api_response import ApiResponse
import json

class ApiSetupPerusahaan(http.Controller):

    @http.route('/api/setup/perusahaan/get', type='http', auth='user', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def get_perusahaan(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            # Retrieve the company (public user defaults to company 1)
            company = request.env.company
            
            data = {
                'id': company.id,
                'name': company.name,
                'street': company.street or '',
                'city': company.city or '',
                'zip': company.zip or '',
                'phone': company.phone or '',
                'mobile': company.mobile or '',
                'email': company.email or '',
                'website': company.website or '',
                'fax': company.idn_fax or '',
                'maks_pelanggan': company.idn_maks_pelanggan or 100,
                'periode_serial': company.idn_periode_serial or '',
                'no_serial': company.idn_no_serial or '',
                'npwp': company.l10n_id_npwp or '',
                'nitku': company.l10n_id_nitku or '',
                'nama_pkp': company.idn_nama_pkp or '',
                'kpp': company.idn_kpp or '',
                'nppkp': company.idn_nppkp or '',
                'tgl_pengukuhan': str(company.idn_tgl_pengukuhan) if company.idn_tgl_pengukuhan else '',
                'alamat_wp': company.idn_alamat_wp or '',
                'kota_wp': company.idn_kota_wp or '',
                'kodepos_wp': company.idn_kodepos_wp or '',
                'tahun_buku_start': company.idn_tahun_buku_start or '1',
                'tahun_buku_end': company.idn_tahun_buku_end or '12',
                'kode_klu': company.idn_kode_klu or '',
                'wajib_ppnbm': company.idn_wajib_ppnbm or False
            }
            return ApiResponse.success(data=data)
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)

    @http.route('/api/setup/perusahaan/save', type='http', auth='user', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    def save_perusahaan(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            return ApiResponse.success()
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            company = request.env.company
            
            # Update company data securely
            update_vals = {}
            if 'name' in data:
                if not data['name']:
                    return ApiResponse.error(message='Nama perusahaan tidak boleh kosong', status_code=400)
                update_vals['name'] = data['name']
            if 'street' in data: update_vals['street'] = data['street']
            if 'city' in data: update_vals['city'] = data['city']
            if 'zip' in data: update_vals['zip'] = data['zip']
            if 'phone' in data: update_vals['phone'] = data['phone']
            if 'mobile' in data: update_vals['mobile'] = data['mobile']
            if 'email' in data: update_vals['email'] = data['email']
            if 'website' in data: update_vals['website'] = data['website']
            if 'fax' in data: update_vals['idn_fax'] = data['fax']
            if 'maks_pelanggan' in data: update_vals['idn_maks_pelanggan'] = data['maks_pelanggan']
            if 'periode_serial' in data: update_vals['idn_periode_serial'] = data['periode_serial']
            if 'no_serial' in data: update_vals['idn_no_serial'] = data['no_serial']
            
            if 'npwp' in data: update_vals['l10n_id_npwp'] = data['npwp']
            if 'nitku' in data: update_vals['l10n_id_nitku'] = data['nitku']
            if 'nama_pkp' in data: update_vals['idn_nama_pkp'] = data['nama_pkp']
            if 'kpp' in data: update_vals['idn_kpp'] = data['kpp']
            if 'nppkp' in data: update_vals['idn_nppkp'] = data['nppkp']
            if 'tgl_pengukuhan' in data and data['tgl_pengukuhan']: update_vals['idn_tgl_pengukuhan'] = data['tgl_pengukuhan']
            if 'alamat_wp' in data: update_vals['idn_alamat_wp'] = data['alamat_wp']
            if 'kota_wp' in data: update_vals['idn_kota_wp'] = data['kota_wp']
            if 'kodepos_wp' in data: update_vals['idn_kodepos_wp'] = data['kodepos_wp']
            if 'tahun_buku_start' in data: update_vals['idn_tahun_buku_start'] = data['tahun_buku_start']
            if 'tahun_buku_end' in data: update_vals['idn_tahun_buku_end'] = data['tahun_buku_end']
            if 'kode_klu' in data: update_vals['idn_kode_klu'] = data['kode_klu']
            if 'wajib_ppnbm' in data: update_vals['idn_wajib_ppnbm'] = data['wajib_ppnbm']

            company.sudo().write(update_vals)
            
            return ApiResponse.success(data={'id': company.id}, message='Data perusahaan berhasil diperbarui')
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)
