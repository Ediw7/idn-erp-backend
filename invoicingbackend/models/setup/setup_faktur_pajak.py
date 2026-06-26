from odoo import models, fields

class FakturPajak(models.Model):
    _name = 'invoicingbackend.faktur_pajak'
    _description = 'Setup Nomor Seri Faktur Pajak'
    _inherit = 'invoicingbackend.base_tenant'

    no_surat = fields.Char(string='Nomor Surat dari KPP', required=True)
    tgl_surat = fields.Date(string='Tgl Surat', required=True)
    tgl_awal = fields.Date(string='Tgl FP Awal', required=True)
    tgl_akhir = fields.Date(string='Tgl FP Akhir', required=True)
    no_seri_awal = fields.Char(string='No Seri FP Awal', required=True)
    no_seri_akhir = fields.Char(string='No Seri FP Akhir', required=True)
