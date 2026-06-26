from odoo import models, fields, api
from odoo.exceptions import ValidationError

class KursPajak(models.Model):
    _name = 'invoicingbackend.kurs_pajak'
    _description = 'Setup Kurs Pajak'
    _inherit = 'invoicingbackend.base_tenant'

    mata_uang_id = fields.Many2one('invoicingbackend.mata_uang', string='Mata Uang', required=True, ondelete='cascade')
    tgl_dari = fields.Date(string='Tgl Dari', required=True)
    tgl_sd = fields.Date(string='Tgl s/d', required=True)
    kurs = fields.Float(string='Kurs', required=True, digits=(16, 4))
    no_kmk = fields.Char(string='No KMK')
    tgl_kmk = fields.Date(string='Tgl KMK')

    @api.constrains('tgl_dari', 'tgl_sd')
    def _check_date_range(self):
        for record in self:
            if record.tgl_sd and record.tgl_dari and record.tgl_sd < record.tgl_dari:
                raise ValidationError("Tanggal Selesai (s/d) tidak boleh lebih kecil dari Tanggal Mulai (Dari).")

    @api.constrains('mata_uang_id', 'tgl_dari', 'tgl_sd', 'company_id')
    def _check_overlap(self):
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('mata_uang_id', '=', record.mata_uang_id.id),
                ('company_id', '=', record.company_id.id),
                '|', '|',
                '&', ('tgl_dari', '<=', record.tgl_dari), ('tgl_sd', '>=', record.tgl_dari),
                '&', ('tgl_dari', '<=', record.tgl_sd), ('tgl_sd', '>=', record.tgl_sd),
                '&', ('tgl_dari', '>=', record.tgl_dari), ('tgl_sd', '<=', record.tgl_sd)
            ]
            overlapping = self.search(domain, limit=1)
            if overlapping:
                raise ValidationError(f"Rentang tanggal kurs pajak bertabrakan dengan kurs yang sudah ada ({overlapping.tgl_dari} s/d {overlapping.tgl_sd}).")
