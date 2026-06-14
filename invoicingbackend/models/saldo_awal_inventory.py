from odoo import models, fields, api

class SaldoAwalInventory(models.Model):
    _name = 'invoicingbackend.saldo_awal_inventory'
    _description = 'Saldo Awal Persediaan'

    gudang_id = fields.Many2one('invoicingbackend.gudang', string='Gudang', required=True)
    tanggal = fields.Date(string='Tanggal', required=True)
    keterangan = fields.Char(string='Keterangan')
    
    line_ids = fields.One2many('invoicingbackend.saldo_awal_inventory_line', 'saldo_awal_id', string='Detail Item')

class SaldoAwalInventoryLine(models.Model):
    _name = 'invoicingbackend.saldo_awal_inventory_line'
    _description = 'Detail Saldo Awal Persediaan'

    saldo_awal_id = fields.Many2one('invoicingbackend.saldo_awal_inventory', string='Saldo Awal', ondelete='cascade')
    item_id = fields.Many2one('invoicingbackend.item', string='Item', required=True)
    quantity = fields.Float(string='Quantity', default=0.0)
    hpp = fields.Float(string='HPP', default=0.0)
    
    @api.depends('quantity', 'hpp')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.hpp
