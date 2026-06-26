from odoo import models, fields

class TandaTangan(models.Model):
    _name = 'invoicingbackend.tanda_tangan'
    _description = 'Setup Tanda Tangan'
    _inherit = 'invoicingbackend.base_tenant'

    jenis_formulir = fields.Char(string='Jenis Formulir', required=True)
    nama = fields.Char(string='Tanda Tangan', required=True)
    jabatan = fields.Char(string='Jabatan')
    lokasi = fields.Char(string='Lokasi')
    ttd_image = fields.Binary(string='Gambar Tanda Tangan', attachment=True)
