from odoo import models, fields

class JenisPajak(models.Model):
    _name = 'invoicingbackend.jenis_pajak'
    _description = 'Setup Kode Jenis Pajak'

    kode = fields.Char(string='Kode', required=True)
    nama = fields.Char(string='Jenis Pajak', required=True)
