from odoo import models, fields, api

class SuratJalan(models.Model):
    _name = 'invoicingbackend.surat_jalan'
    _description = 'Surat Jalan'
    _inherit = 'invoicingbackend.base_tenant'

    no_sj = fields.Char(string='No Surat Jalan', required=True)
    tgl_sj = fields.Date(string='Tanggal', required=True, default=fields.Date.context_today)
    pelanggan_id = fields.Many2one('invoicingbackend.pelanggan', string='Nama Pelanggan', required=True)
    alamat_kirim = fields.Text(string='Alamat Kirim')
    
    gudang_id = fields.Many2one('invoicingbackend.gudang', string='Gudang')
    so_id = fields.Many2one('invoicingbackend.sales_order', string='No. Sales Order')
    no_po = fields.Char(string='No. PO')
    no_kendaraan = fields.Char(string='No. Kendaraan')
    no_invoice = fields.Char(string='No. Invoice')
    keterangan = fields.Text(string='Keterangan')
    
    line_ids = fields.One2many('invoicingbackend.surat_jalan_line', 'sj_id', string='Detail Surat Jalan')

class SuratJalanLine(models.Model):
    _name = 'invoicingbackend.surat_jalan_line'
    _description = 'Surat Jalan Line'
    _inherit = 'invoicingbackend.base_tenant'

    sj_id = fields.Many2one('invoicingbackend.surat_jalan', string='Surat Jalan', ondelete='cascade')
    item_id = fields.Many2one('invoicingbackend.item', string='Kode Barang', required=True)
    nama_barang = fields.Char(related='item_id.nama', string='Nama Barang', readonly=True)
    satuan = fields.Char(string='Satuan')
    kuantum = fields.Float(string='Kuantum', default=1.0)
    keterangan = fields.Char(string='Keterangan')
