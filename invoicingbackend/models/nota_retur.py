from odoo import models, fields, api

class NotaRetur(models.Model):
    _name = 'invoicingbackend.nota_retur'
    _description = 'Nota Retur Penjualan'

    no_nota = fields.Char(string="No Nota Retur")
    tgl_nota = fields.Date(string="Tgl Nota Retur")
    pelanggan_id = fields.Many2one('invoicingbackend.setup_pelanggan', string="Pelanggan")
    alamat_pembeli = fields.Text(string="Alamat Pembeli")
    jenis_transaksi = fields.Char(string="Jenis Transaksi")
    gudang_id = fields.Char(string="Gudang")
    jenis_retur = fields.Char(string="Jenis Retur")
    atas_no_fp = fields.Char(string="Atas No FP")
    tgl_fp = fields.Date(string="Tgl FP")
    atas_no_invoice = fields.Char(string="Atas No Invoice")
    mata_uang_id = fields.Many2one('invoicingbackend.setup_mata_uang', string="Mata Uang")
    tarif_ppn = fields.Float(string="Tarif PPN")
    kurs_pajak = fields.Float(string="Kurs Pajak")
    lokasi_pelaporan = fields.Char(string="Lokasi Pelaporan")
    tanda_tangan = fields.Char(string="Tanda Tangan")
    jabatan = fields.Char(string="Jabatan")
    
    line_ids = fields.One2many('invoicingbackend.nota_retur_line', 'nota_id', string="Lines")

class NotaReturLine(models.Model):
    _name = 'invoicingbackend.nota_retur_line'
    _description = 'Nota Retur Penjualan Line'

    nota_id = fields.Many2one('invoicingbackend.nota_retur', string="Nota Retur", ondelete='cascade')
    item_id = fields.Many2one('invoicingbackend.setup_item', string="Item")
    nama_barang = fields.Char(string="Nama Barang")
    satuan = fields.Char(string="Satuan")
    kuantum = fields.Float(string="Kuantum")
    harga_satuan = fields.Float(string="Harga Satuan")
    harga_jual = fields.Float(string="Harga Jual")
    hpp = fields.Float(string="HPP")
    total_hpp = fields.Float(string="Total HPP")
