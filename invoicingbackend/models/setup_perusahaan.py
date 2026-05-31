from odoo import models, fields

class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    # Perpajakan
    l10n_id_npwp = fields.Char(string='NPWP Perusahaan', size=25, help="Nomor Pokok Wajib Pajak")
    l10n_id_nitku = fields.Char(string='NITKU', size=22, help='Nomor Identitas Tempat Kegiatan Usaha')
    
    idn_nama_pkp = fields.Char(string='Nama PKP')
    idn_kpp = fields.Char(string='KPP')
    idn_nppkp = fields.Char(string='NPPKP')
    idn_tgl_pengukuhan = fields.Date(string='Tgl Pengukuhan')
    idn_alamat_wp = fields.Text(string='Alamat Wajib Pajak')
    idn_kota_wp = fields.Char(string='Kota WP')
    idn_kodepos_wp = fields.Char(string='Kode Pos WP')
    idn_tahun_buku_start = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Tahun Buku Awal', default='1')
    idn_tahun_buku_end = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Tahun Buku Akhir', default='12')
    idn_kode_klu = fields.Char(string='Kode KLU')
    idn_wajib_ppnbm = fields.Boolean(string='Wajib PPnBM', default=False)
    
    # Krishand Legacy Profil Fields
    idn_fax = fields.Char(string='No. Fax')
    idn_maks_pelanggan = fields.Integer(string='Maks. Jlh Pelanggan', default=100)
    idn_periode_serial = fields.Char(string='Periode Serial', default='202012')
    idn_no_serial = fields.Char(string='No. Serial', default='KR-27119392114408')
