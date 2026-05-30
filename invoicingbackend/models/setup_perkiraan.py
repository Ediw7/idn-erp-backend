from odoo import models, fields

class Perkiraan(models.Model):
    _name = 'invoicingbackend.perkiraan'
    _description = 'Setup Perkiraan'

    no_perkiraan = fields.Char(string='No Perkiraan', required=True)
    nama_perkiraan = fields.Char(string='Nama Perkiraan', required=True)
    kas_bank = fields.Boolean(string='Kas/Bank', default=False)
