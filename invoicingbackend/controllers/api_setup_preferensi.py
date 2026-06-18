from odoo import http
from odoo.http import request

class ApiSetupPreferensi(http.Controller):
    @http.route('/api/setup/preferensi/get', type='json', auth='user', methods=['POST'], cors='*')
    def get_preferensi(self, **kw):
        try:
            pref = request.env['invoicingbackend.preferensi'].get_preferences()
            return {'status': 'success', 'data': pref}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/setup/preferensi/save', type='json', auth='user', methods=['POST'], cors='*')
    def save_preferensi(self, **kw):
        data = kw
        try:
            pref = request.env['invoicingbackend.preferensi'].search([], limit=1)
            
            # Map frontend camelCase to backend snake_case
            update_vals = {
                'folder_database': data.get('folderDatabase'),
                'file_database': data.get('fileDatabase'),
                'folder_backup_data': data.get('folderBackupData'),
                'folder_csv_faktur': data.get('folderCsvFaktur'),
                'nama_file_logo': data.get('namaFileLogo'),
                'lebar_logo': data.get('lebarLogo'),
                'tinggi_logo': data.get('tinggiLogo'),
                'dokumen_pemotongan_inventory': data.get('dokumenPemotonganInventory'),
                'validasi_qty_minus_sj': data.get('validasiQtyMinusSj'),
                'validasi_qty_minus_so': data.get('validasiQtyMinusSo'),
                'tarif_ppn': data.get('tarifPpn'),
                'tarif_pph22': data.get('tarifPph22'),
                'kode_cabang_fp': data.get('kodeCabangFp'),
                'selisih_hari_invoice_faktur': data.get('selisihHariInvoiceFaktur'),
                'notif_sisa_faktur_kurang_dari': data.get('notifSisaFakturKurangDari'),
                'desimal_kuantum': data.get('desimalKuantum'),
                'desimal_harga_satuan': data.get('desimalHargaSatuan'),
                'desimal_jumlah': data.get('desimalJumlah'),
                'umur_piutang_1_sd': data.get('umurPiutang1Sd'),
                'umur_piutang_2_mulai': data.get('umurPiutang2Mulai'),
                'umur_piutang_2_sd': data.get('umurPiutang2Sd'),
                'umur_piutang_3_mulai': data.get('umurPiutang3Mulai'),
                'umur_piutang_3_sd': data.get('umurPiutang3Sd'),
                'umur_piutang_4_mulai': data.get('umurPiutang4Mulai'),
                'umur_piutang_4_sd': data.get('umurPiutang4Sd'),
                'umur_piutang_5_mulai': data.get('umurPiutang5Mulai'),
                'perk_piutang': data.get('perkPiutang'),
                'perk_penjualan': data.get('perkPenjualan'),
                'perk_uang_muka_penj': data.get('perkUangMukaPenj'),
                'perk_disc_penjualan': data.get('perkDiscPenjualan'),
                'perk_ppn': data.get('perkPpn'),
                'perk_pph22': data.get('perkPph22'),
                'ket_lembar_3_fp': data.get('ketLembar3Fp'),
                'ket_lembar_4_fp': data.get('ketLembar4Fp'),
                'footer_invoice_vat': data.get('footerInvoiceVat'),
                'footer_invoice_non_vat': data.get('footerInvoiceNonVat'),
                'footer_kwitansi_vat': data.get('footerKwitansiVat'),
                'footer_kwitansi_non_vat': data.get('footerKwitansiNonVat'),
            }
            
            if not pref:
                update_vals['company_id'] = request.env.user.company_id.id
                request.env['invoicingbackend.preferensi'].create(update_vals)
            else:
                pref.write(update_vals)
                
            return {'status': 'success', 'message': 'Setup preferensi berhasil disimpan!'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
