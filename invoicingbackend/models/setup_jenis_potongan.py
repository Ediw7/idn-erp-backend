from odoo import models, fields

class JenisPotongan(models.Model):
    _name = 'invoicingbackend.jenis_potongan'
    _description = 'Setup Jenis Potongan'

    kode = fields.Char(string='Kode', required=True)
    nama = fields.Char(string='Jenis Potongan', required=True)
    perkiraan_id = fields.Many2one('invoicingbackend.perkiraan', string='No Perkiraan', ondelete='set null')
