from odoo import models, fields


class Proyek(models.Model):
    _name = "invoicingbackend.proyek"
    _description = "Setup Proyek"
    _inherit = "invoicingbackend.base_tenant"

    kode = fields.Char(string="Kode", required=True)
    nama = fields.Char(string="Proyek", required=True)
