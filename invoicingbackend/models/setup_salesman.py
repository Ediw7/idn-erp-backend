from odoo import models, fields

class Salesman(models.Model):
    _name = 'invoicingbackend.salesman'
    _description = 'Setup Salesman'

    kode = fields.Char(string='Kode', required=True)
    nama = fields.Char(string='Nama Salesman', required=True)
