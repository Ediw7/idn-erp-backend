from odoo import models, fields, api


class MataUang(models.Model):
    _name = "invoicingbackend.mata_uang"
    _description = "Setup Mata Uang"
    _inherit = "invoicingbackend.base_tenant"

    kode = fields.Char(string="Kode", required=True)
    nama = fields.Char(string="Mata Uang", required=True)
    per = fields.Char(string="Per")
