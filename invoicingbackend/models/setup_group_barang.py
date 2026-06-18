from odoo import models, fields

class GroupBarang(models.Model):
    _name = 'invoicingbackend.group_barang'
    _description = 'Setup Group Barang'
    _inherit = 'invoicingbackend.base_tenant'

    nama = fields.Char(string='Group Barang', required=True)
