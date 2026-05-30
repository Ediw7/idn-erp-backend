from odoo import models, fields

class KursPajak(models.Model):
    _name = 'invoicingbackend.kurs_pajak'
    _description = 'Setup Kurs Pajak'

    mata_uang_id = fields.Many2one('invoicingbackend.mata_uang', string='Mata Uang', required=True, ondelete='cascade')
    tgl_dari = fields.Date(string='Tgl Dari', required=True)
    tgl_sd = fields.Date(string='Tgl s/d', required=True)
    kurs = fields.Float(string='Kurs', required=True, digits=(16, 4))
    no_kmk = fields.Char(string='No KMK')
    tgl_kmk = fields.Date(string='Tgl KMK')
