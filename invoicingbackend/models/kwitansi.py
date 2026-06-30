from odoo import models, fields

class Kwitansi(models.Model):
    _name = 'invoicingbackend.kwitansi'
    _description = 'Kwitansi Pembayaran'
    _inherit = 'invoicingbackend.base_tenant'

    no_kwitansi = fields.Char(string='No. Kwitansi', required=True, index=True)
    tgl_kwitansi = fields.Date(string='Tgl Kwitansi', required=True, default=fields.Date.context_today)
    jenis = fields.Selection([
        ('VAT', 'VAT'),
        ('Non-VAT', 'Non-VAT')
    ], string='Jenis Kwitansi', default='VAT')
    
    invoice_id = fields.Many2one('invoicingbackend.invoice', string='Dari Invoice', ondelete='restrict')
    pelanggan_id = fields.Many2one('invoicingbackend.pelanggan', string='Sudah Terima Dari', required=True)
    
    mata_uang = fields.Selection([
        ('IDR', 'IDR'),
        ('USD', 'USD')
    ], string='Mata Uang', default='IDR')
    jumlah = fields.Float(string='Jumlah', required=True, default=0.0)
    terbilang = fields.Char(string='Terbilang')
    
    untuk_pembayaran = fields.Text(string='Untuk Pembayaran')
    keterangan_footer = fields.Text(string='Keterangan Footer')
    
    penandatangan = fields.Char(string='Nama Penandatangan')
    jabatan = fields.Char(string='Jabatan')
