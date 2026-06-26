from odoo import models, fields

class Pelanggan(models.Model):
    _name = 'invoicingbackend.pelanggan'
    _description = 'Setup Pelanggan'
    _inherit = 'invoicingbackend.base_tenant'

    kode = fields.Char(string='Kode Pelanggan', required=True)
    is_ekspor = fields.Boolean(string='Ekspor', default=False)
    nama = fields.Char(string='Nama Pelanggan', required=True)
    alamat = fields.Text(string='Alamat Pelanggan')
    telepon = fields.Char(string='No. Telepon')
    fax = fields.Char(string='No. Fax')
    
    alamat_kirim = fields.Text(string='Alamat Pengiriman')
    telepon_kirim = fields.Char(string='No. Telepon Pengiriman')
    fax_kirim = fields.Char(string='No. Fax Pengiriman')
    
    nama_wp = fields.Char(string='Nama Wajib Pajak')
    npwp = fields.Char(string='NPWP')
    nik = fields.Char(string='No KTP')
    alamat_wp = fields.Text(string='Alamat Wajib Pajak')
    
    jenis_transaksi = fields.Selection([
        ('01', 'Kepada Bukan Pemungut PPN (01)'),
        ('02', 'Kepada Pemungut Bendaharawan (02)'),
        ('03', 'Kepada Pemungut Selain Bendaharawan (03)'),
        ('04', 'DPP Nilai Lain (04)'),
        ('06', 'Penyerahan Lainnya (06)'),
        ('07', 'Penyerahan yang Tidak Dipungut PPN (07)'),
        ('08', 'Penyerahan yang Dibebaskan dari Pengenaan PPN (08)'),
        ('09', 'Penyerahan Aktiva (09)')
    ], string='Jenis Transaksi', default='01')
    
    ket_tambahan = fields.Char(string='Ket Tambahan')
    email = fields.Char(string='Email')
    contact_person = fields.Char(string='Contact Person')
    no_hp = fields.Char(string='No HP')
    jabatan = fields.Char(string='Jabatan')
    
    pembayaran_id = fields.Many2one('invoicingbackend.pembayaran', string='Cara Pembayaran', ondelete='set null')
    tingkat_harga = fields.Selection([
        ('1', 'Harga Jual 1'),
        ('2', 'Harga Jual 2'),
        ('3', 'Harga Jual 3')
    ], string='Tingkatan Harga Jual', default='1')
    diskon = fields.Float(string='Discount Harga Jual (%)', default=0.0)
    perk_piutang_id = fields.Many2one('invoicingbackend.perkiraan', string='No Perkiraan Piutang', ondelete='set null')
    keterangan = fields.Text(string='Keterangan')
