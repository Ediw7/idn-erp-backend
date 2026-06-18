from odoo import models, fields, api

class NotaReturPembelian(models.Model):
    _name = 'invoicingbackend.nota_retur_pembelian'
    _description = 'Nota Retur Pembelian'
    _inherit = 'invoicingbackend.base_tenant'

    no_nota = fields.Char(string="No Nota Retur")
    tgl_nota = fields.Date(string="Tgl Nota Retur")
    supplier_id = fields.Many2one('invoicingbackend.setup_supplier', string="Supplier")
    alamat_penjual = fields.Text(string="Alamat Penjual")
    jenis_retur = fields.Char(string="Jenis Retur")
    gudang_id = fields.Char(string="Gudang")
    atas_no_fp = fields.Char(string="Atas No FP")
    tgl_fp = fields.Date(string="Tgl FP")
    mata_uang_id = fields.Many2one('invoicingbackend.setup_mata_uang', string="Mata Uang")
    kurs_pajak = fields.Float(string="Kurs Pajak")
    tarif_ppn = fields.Float(string="Tarif PPN")
    jenis_transaksi = fields.Char(string="Jenis Transaksi")
    status = fields.Char(string="Status")
    
    tanda_tangan = fields.Char(string="Tanda Tangan")
    jabatan = fields.Char(string="Jabatan")
    
    line_ids = fields.One2many('invoicingbackend.nota_retur_pembelian_line', 'nota_id', string="Lines")

class NotaReturPembelianLine(models.Model):
    _name = 'invoicingbackend.nota_retur_pembelian_line'
    _description = 'Nota Retur Pembelian Line'
    _inherit = 'invoicingbackend.base_tenant'

    nota_id = fields.Many2one('invoicingbackend.nota_retur_pembelian', string="Nota Retur", ondelete='cascade')
    item_id = fields.Many2one('invoicingbackend.setup_item', string="Item")
    nama_barang = fields.Char(string="Nama Barang")
    satuan = fields.Char(string="Satuan")
    kuantum = fields.Float(string="Kuantum")
    harga_satuan = fields.Float(string="Harga Satuan")
    harga_jual = fields.Float(string="Harga Jual") # Keeps legacy naming from screenshot
