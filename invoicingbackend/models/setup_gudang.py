from odoo import models, fields, api

class Gudang(models.Model):
    _name = 'invoicingbackend.gudang'
    _description = 'Setup Gudang'

    kode_gudang = fields.Char(string='Kode Gudang', required=True)
    nama_gudang = fields.Char(string='Nama Gudang', required=True)
    lokasi = fields.Char(string='Lokasi')
    is_default = fields.Boolean(string='Default', default=False)
