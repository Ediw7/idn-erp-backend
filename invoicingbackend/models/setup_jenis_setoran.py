from odoo import models, fields

class JenisSetoran(models.Model):
    _name = 'invoicingbackend.jenis_setoran'
    _description = 'Setup Kode Jenis Setoran'

    jenis_pajak_id = fields.Many2one('invoicingbackend.jenis_pajak', string='MAP', required=True, ondelete='cascade')
    kode = fields.Char(string='Kode Setoran', required=True)
    nama = fields.Char(string='Jenis Setoran', required=True)
