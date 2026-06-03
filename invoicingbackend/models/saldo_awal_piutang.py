from odoo import models, fields, api

class SaldoAwalPiutang(models.Model):
    _name = 'invoicingbackend.saldo_awal_piutang'
    _description = 'Saldo Awal Piutang'

    no_invoice = fields.Char(string='No. Invoice', required=True)
    tanggal = fields.Date(string='Tanggal', required=True)
    pelanggan_id = fields.Many2one('invoicingbackend.pelanggan', string='Pelanggan', required=True)
    proyek_id = fields.Many2one('invoicingbackend.proyek', string='Proyek')
    tgl_jt = fields.Date(string='Tgl JT')
    mata_uang_id = fields.Many2one('invoicingbackend.mata_uang', string='Ccy')
    saldo_invoice = fields.Float(string='Saldo Invoice', required=True, default=0.0)
    is_paid = fields.Boolean(string='Paid', default=False)
