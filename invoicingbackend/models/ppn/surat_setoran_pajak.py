from odoo import models, fields, api

class SuratSetoranPajak(models.Model):
    _name = 'invoicingbackend.surat_setoran_pajak'
    _description = 'Surat Setoran Pajak'
    _inherit = 'invoicingbackend.base_tenant'

    kpp = fields.Char(string="KPP")
    nama_wp = fields.Char(string="Nama WP")
    npwp = fields.Char(string="NPWP")
    alamat = fields.Text(string="Alamat")
    kode_pos = fields.Char(string="Kode Pos")
    
    tahun = fields.Char(string="Tahun", default="2020")
    bulan = fields.Selection([
        ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'), ('04', 'April'),
        ('05', 'Mei'), ('06', 'Juni'), ('07', 'Juli'), ('08', 'Agustus'),
        ('09', 'September'), ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], string="Bulan")
    
    kode_jenis_pajak = fields.Char(string="Kode Jenis Pajak")
    kode_jenis_pajak_desc = fields.Char(string="Desc Jenis Pajak")
    
    kode_jenis_setoran = fields.Char(string="Kode Jenis Setoran")
    kode_jenis_setoran_desc = fields.Char(string="Desc Jenis Setoran")
    
    uraian_pembayaran = fields.Text(string="Uraian Pembayaran")
    
    no_ketetapan = fields.Char(string="No Ketetapan")
    ntpp = fields.Char(string="NTPP")
    
    jumlah = fields.Float(string="Jumlah")
    tanggal = fields.Date(string="Tanggal")
    
    tanda_tangan = fields.Char(string="Tanda Tangan")
    keterangan = fields.Char(string="Keterangan")
    
    ssp_pemungut = fields.Boolean(string="SSP Pemungut", default=False)
