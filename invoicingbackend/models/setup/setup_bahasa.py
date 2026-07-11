from odoo import models, fields


class Bahasa(models.Model):
    _name = "invoicingbackend.bahasa"
    _description = "Setup Bahasa"
    _inherit = "invoicingbackend.base_tenant"

    jenis_objek = fields.Char(string="Jenis", required=True)
    nama_objek = fields.Char(string="Nama Objek", required=True)
    default_sistem = fields.Char(string="Default dari Sistem", required=True)
    judul_kustom = fields.Char(string="Judul yang Diinginkan")
