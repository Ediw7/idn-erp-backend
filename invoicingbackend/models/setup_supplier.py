from odoo import models, fields

class Supplier(models.Model):
    _name = 'invoicingbackend.supplier'
    _description = 'Setup Supplier'

    kode = fields.Char(string='Kode Supplier', required=True)
    nama = fields.Char(string='Nama Supplier', required=True)
    alamat = fields.Text(string='Alamat Supplier')
    telepon = fields.Char(string='Nomor Telepon')
    fax = fields.Char(string='Nomor Fax')
    email = fields.Char(string='E-mail')
    contact_person = fields.Char(string='Contact Person')
    no_hp = fields.Char(string='No. HP')
    
    nama_wp = fields.Char(string='Nama Wajib Pajak')
    alamat_wp = fields.Text(string='Alamat Wajib Pajak')
    npwp = fields.Char(string='NPWP')
    tgl_pengukuhan = fields.Date(string='Tgl Pengukuhan')
    no_seri_fp_masukan = fields.Char(string='No. Seri FP Masukan')
    is_pkp = fields.Boolean(string='Apakah PKP ?', default=False)
    
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
    
    pembayaran_id = fields.Many2one('invoicingbackend.pembayaran', string='Cara Pembayaran', ondelete='set null')
    keterangan = fields.Text(string='Keterangan')
