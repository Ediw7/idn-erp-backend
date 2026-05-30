import json
from odoo import http
from odoo.http import request, Response

class SetupController(http.Controller):

    @http.route('/api/setup/perusahaan', type='http', auth='public', methods=['GET', 'POST', 'OPTIONS'], csrf=False, cors='*')
    def setup_perusahaan(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200)

        # Retrieve the company (public user defaults to company 1)
        company = request.env.company

        if request.httprequest.method == 'GET':
            try:
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
                    'fax': company.krishand_fax or '',
                    'maks_pelanggan': company.krishand_maks_pelanggan or 100,
                    'periode_serial': company.krishand_periode_serial or '',
                    'no_serial': company.krishand_no_serial or '',
                    'npwp': company.l10n_id_npwp or '',
                    'nitku': company.l10n_id_nitku or '',
                    'nama_pkp': company.krishand_nama_pkp or '',
                    'kpp': company.krishand_kpp or '',
                    'nppkp': company.krishand_nppkp or '',
                    'tgl_pengukuhan': str(company.krishand_tgl_pengukuhan) if company.krishand_tgl_pengukuhan else '',
                    'alamat_wp': company.krishand_alamat_wp or '',
                    'kota_wp': company.krishand_kota_wp or '',
                    'kodepos_wp': company.krishand_kodepos_wp or '',
                    'tahun_buku_start': company.krishand_tahun_buku_start or '1',
                    'tahun_buku_end': company.krishand_tahun_buku_end or '12',
                    'kode_klu': company.krishand_kode_klu or '',
                    'wajib_ppnbm': company.krishand_wajib_ppnbm or False
                }
                return Response(
                    json.dumps(data), 
                    status=200, 
                    content_type='application/json'
                )
            except Exception as e:
                return Response(
                    json.dumps({'error': str(e)}), 
                    status=500, 
                    content_type='application/json'
                )

        elif request.httprequest.method == 'POST':
            try:
                data = json.loads(request.httprequest.data.decode('utf-8'))
                
                # Update company data securely
                update_vals = {}
                if 'name' in data: update_vals['name'] = data['name']
                if 'street' in data: update_vals['street'] = data['street']
                if 'city' in data: update_vals['city'] = data['city']
                if 'zip' in data: update_vals['zip'] = data['zip']
                if 'phone' in data: update_vals['phone'] = data['phone']
                if 'mobile' in data: update_vals['mobile'] = data['mobile']
                if 'email' in data: update_vals['email'] = data['email']
                if 'website' in data: update_vals['website'] = data['website']
                if 'fax' in data: update_vals['krishand_fax'] = data['fax']
                # maks_pelanggan, periode_serial, no_serial are intentionally excluded to prevent tampering by users.
                if 'npwp' in data: update_vals['l10n_id_npwp'] = data['npwp']
                if 'nitku' in data: update_vals['l10n_id_nitku'] = data['nitku']
                
                if 'nama_pkp' in data: update_vals['krishand_nama_pkp'] = data['nama_pkp']
                if 'kpp' in data: update_vals['krishand_kpp'] = data['kpp']
                if 'nppkp' in data: update_vals['krishand_nppkp'] = data['nppkp']
                if 'tgl_pengukuhan' in data and data['tgl_pengukuhan']: update_vals['krishand_tgl_pengukuhan'] = data['tgl_pengukuhan']
                if 'alamat_wp' in data: update_vals['krishand_alamat_wp'] = data['alamat_wp']
                if 'kota_wp' in data: update_vals['krishand_kota_wp'] = data['kota_wp']
                if 'kodepos_wp' in data: update_vals['krishand_kodepos_wp'] = data['kodepos_wp']
                if 'tahun_buku_start' in data: update_vals['krishand_tahun_buku_start'] = data['tahun_buku_start']
                if 'tahun_buku_end' in data: update_vals['krishand_tahun_buku_end'] = data['tahun_buku_end']
                if 'kode_klu' in data: update_vals['krishand_kode_klu'] = data['kode_klu']
                if 'wajib_ppnbm' in data: update_vals['krishand_wajib_ppnbm'] = data['wajib_ppnbm']

                company.sudo().write(update_vals)

                return Response(
                    json.dumps({'message': 'Data perusahaan berhasil diperbarui', 'id': company.id}), 
                    status=200, 
                    content_type='application/json'
                )
            except Exception as e:
                return Response(
                    json.dumps({'error': str(e)}), 
                    status=500, 
                    content_type='application/json'
                )
