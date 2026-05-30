from odoo import models, fields

class ResCompanyExt(models.Model):
    _inherit = 'res.company'

    # Perpajakan
    l10n_id_npwp = fields.Char(string='NPWP Perusahaan', size=25, help="Nomor Pokok Wajib Pajak")
    l10n_id_nitku = fields.Char(string='NITKU', size=22, help='Nomor Identitas Tempat Kegiatan Usaha')
    
    krishand_nama_pkp = fields.Char(string='Nama PKP')
    krishand_kpp = fields.Char(string='KPP')
    krishand_nppkp = fields.Char(string='NPPKP')
    krishand_tgl_pengukuhan = fields.Date(string='Tgl Pengukuhan')
    krishand_alamat_wp = fields.Text(string='Alamat Wajib Pajak')
    krishand_kota_wp = fields.Char(string='Kota WP')
    krishand_kodepos_wp = fields.Char(string='Kode Pos WP')
    krishand_tahun_buku_start = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Tahun Buku Awal', default='1')
    krishand_tahun_buku_end = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Tahun Buku Akhir', default='12')
    krishand_kode_klu = fields.Char(string='Kode KLU')
    krishand_wajib_ppnbm = fields.Boolean(string='Wajib PPnBM', default=False)
    
    # Krishand Legacy Profil Fields
    krishand_fax = fields.Char(string='No. Fax')
    krishand_maks_pelanggan = fields.Integer(string='Maks. Jlh Pelanggan', default=100)
    krishand_periode_serial = fields.Char(string='Periode Serial', default='202012')
    krishand_no_serial = fields.Char(string='No. Serial', default='KR-27119392114408')
