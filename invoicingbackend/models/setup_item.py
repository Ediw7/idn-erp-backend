from odoo import models, fields

class Item(models.Model):
    _name = 'invoicingbackend.item'
    _description = 'Setup Item'

    kode = fields.Char(string='Kode', required=True)
    nama = fields.Char(string='Nama Item', required=True)
    group_barang_id = fields.Many2one('invoicingbackend.group_barang', string='Group Item', ondelete='set null')
    satuan = fields.Char(string='Satuan', default='Pcs')
    harga_jual_1 = fields.Float(string='Harga Jual 1', default=0.0)
    harga_jual_2 = fields.Float(string='Harga Jual 2', default=0.0)
    harga_jual_3 = fields.Float(string='Harga Jual 3', default=0.0)
    supplier_utama = fields.Char(string='Supplier Utama')
    perk_penjualan_id = fields.Many2one('invoicingbackend.perkiraan', string='Perk Penjualan', ondelete='set null')
    perk_hpp_id = fields.Many2one('invoicingbackend.perkiraan', string='Perk HPP', ondelete='set null')
    is_inventory = fields.Boolean(string='Inventory', default=True)
