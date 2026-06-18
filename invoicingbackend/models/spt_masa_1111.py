from odoo import models, fields, api

class SptMasa1111(models.Model):
    _name = 'invoicingbackend.spt_masa_1111'
    _description = 'SPT Masa PPN 1111'
    _inherit = 'invoicingbackend.base_tenant'

    tahun = fields.Char(string="Tahun", default="2020")
    masa_awal = fields.Selection([
        ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'), ('04', 'April'),
        ('05', 'Mei'), ('06', 'Juni'), ('07', 'Juli'), ('08', 'Agustus'),
        ('09', 'September'), ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], string="Masa Awal", default='01')
    masa_akhir = fields.Selection([
        ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'), ('04', 'April'),
        ('05', 'Mei'), ('06', 'Juni'), ('07', 'Juli'), ('08', 'Agustus'),
        ('09', 'September'), ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], string="Masa Akhir", default='01')
    pembetulan_ke = fields.Integer(string="Pembetulan Ke", default=0)
    tanggal_spt = fields.Date(string="Tanggal SPT")
    is_locked = fields.Boolean(string="Locked", default=False)

    # I. PENYERAHAN BARANG DAN JASA
    dpp_ekspor = fields.Float(string="DPP Ekspor", default=0)
    ppn_ekspor = fields.Float(string="PPN Ekspor", default=0)
    
    dpp_dipungut_sendiri = fields.Float(string="DPP Dipungut Sendiri", default=0)
    ppn_dipungut_sendiri = fields.Float(string="PPN Dipungut Sendiri", default=0)
    
    dpp_dipungut_pemungut = fields.Float(string="DPP Dipungut Pemungut", default=0)
    ppn_dipungut_pemungut = fields.Float(string="PPN Dipungut Pemungut", default=0)
    
    dpp_tidak_dipungut = fields.Float(string="DPP Tidak Dipungut", default=0)
    ppn_tidak_dipungut = fields.Float(string="PPN Tidak Dipungut", default=0)
    
    dpp_dibebaskan = fields.Float(string="DPP Dibebaskan", default=0)
    ppn_dibebaskan = fields.Float(string="PPN Dibebaskan", default=0)

    dpp_tidak_terutang = fields.Float(string="DPP Tidak Terutang PPN", default=0)

    # II. PENGHITUNGAN PPN KURANG BAYAR/LEBIH BAYAR
    ppn_disetor_dimuka = fields.Float(string="PPN Disetor Dimuka", default=0)
    pajak_masukan_diperhitungkan = fields.Float(string="Pajak Masukan", default=0)
    ppn_spt_dibetulkan = fields.Float(string="PPN SPT Dibetulkan", default=0)
    
    tgl_lunas_kurang_bayar = fields.Date(string="Tgl Lunas")
    ntpn_kurang_bayar = fields.Char(string="NTPN Lunas")

    lebih_bayar_pada = fields.Selection([('1.1', 'Butir II.D'), ('1.2', 'Butir II.F')], string="Lebih Bayar Pada")
    lebih_bayar_oleh = fields.Selection([('2.1', 'PKP Pasal 9(4b)'), ('2.2', 'Selain PKP Pasal 9(4b)')], string="Lebih Bayar Oleh")
    lebih_bayar_diminta_untuk = fields.Selection([
        ('3.1_next', 'Kompensasi Masa Berikutnya'), 
        ('3.1_other', 'Kompensasi Masa Lain'), 
        ('3.2', 'Dikembalikan (Restitusi)')
    ], string="Diminta Untuk")
    
    kompensasi_masa = fields.Selection([
        ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'), ('04', 'April'),
        ('05', 'Mei'), ('06', 'Juni'), ('07', 'Juli'), ('08', 'Agustus'),
        ('09', 'September'), ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], string="Kompensasi Masa Lain")
    kompensasi_tahun = fields.Char(string="Kompensasi Tahun Lain")

    restitusi_pasal_17c = fields.Selection([('biasa', 'Prosedur Biasa'), ('pendahuluan', 'Pengembalian Pendahuluan')], string="Pasal 17C KUP")
    restitusi_pasal_17d = fields.Selection([('biasa', 'Prosedur Biasa'), ('pendahuluan', 'Pengembalian Pendahuluan')], string="Pasal 17D KUP")
    restitusi_pasal_9_4c = fields.Boolean(string="Pasal 9 (4c) PPN")

    # III. PPN TERUTANG ATAS KEGIATAN MEMBANGUN SENDIRI
    membangun_dpp = fields.Float(string="Membangun DPP", default=0)
    membangun_ppn = fields.Float(string="Membangun PPN", default=0)
