from odoo import models, fields

class Pembayaran(models.Model):
    _name = 'invoicingbackend.pembayaran'
    _description = 'Setup Cara Pembayaran'
    _inherit = 'invoicingbackend.base_tenant'

    kode = fields.Char(string='Kode', required=True)
    nama = fields.Char(string='Cara Pembayaran', required=True)
    hari_jatuh_tempo = fields.Integer(string='Jlh Hari JT', default=0)
