from odoo import models, fields


class FormatBukti(models.Model):
    _name = "invoicingbackend.format_bukti"
    _description = "Setup Format No Bukti"
    _inherit = "invoicingbackend.base_tenant"

    periode = fields.Char(string="Periode (yyyymm)", required=True)

    # Line 1
    inv_vat_prefiks = fields.Char(string="Invoice VAT Prefiks")
    inv_vat_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Invoice VAT Digit",
        default="3",
    )
    inv_vat_sufiks = fields.Char(string="Invoice VAT Sufiks")

    inv_non_vat_prefiks = fields.Char(string="Invoice Non-VAT Prefiks")
    inv_non_vat_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Invoice Non-VAT Digit",
        default="3",
    )
    inv_non_vat_sufiks = fields.Char(string="Invoice Non-VAT Sufiks")

    kwi_vat_prefiks = fields.Char(string="Kwitansi VAT Prefiks")
    kwi_vat_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Kwitansi VAT Digit",
        default="3",
    )
    kwi_vat_sufiks = fields.Char(string="Kwitansi VAT Sufiks")

    kwi_non_vat_prefiks = fields.Char(string="Kwitansi Non-VAT Prefiks")
    kwi_non_vat_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Kwitansi Non-VAT Digit",
        default="3",
    )
    kwi_non_vat_sufiks = fields.Char(string="Kwitansi Non-VAT Sufiks")

    # Line 2
    pem_inv_prefiks = fields.Char(string="Pembayaran Invoice Prefiks")
    pem_inv_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Pembayaran Invoice Digit",
        default="3",
    )
    pem_inv_sufiks = fields.Char(string="Pembayaran Invoice Sufiks")

    nota_kredit_prefiks = fields.Char(string="Nota Kredit Prefiks")
    nota_kredit_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Nota Kredit Digit",
        default="3",
    )
    nota_kredit_sufiks = fields.Char(string="Nota Kredit Sufiks")

    so_prefiks = fields.Char(string="Sales Order Prefiks")
    so_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Sales Order Digit",
        default="3",
    )
    so_sufiks = fields.Char(string="Sales Order Sufiks")

    sj_prefiks = fields.Char(string="Surat Jalan Prefiks")
    sj_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Surat Jalan Digit",
        default="3",
    )
    sj_sufiks = fields.Char(string="Surat Jalan Sufiks")

    # Line 3
    retur_jual_prefiks = fields.Char(string="Retur Penjualan Prefiks")
    retur_jual_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Retur Penjualan Digit",
        default="3",
    )
    retur_jual_sufiks = fields.Char(string="Retur Penjualan Sufiks")

    retur_beli_prefiks = fields.Char(string="Retur Pembelian Barang Prefiks")
    retur_beli_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Retur Pembelian Barang Digit",
        default="3",
    )
    retur_beli_sufiks = fields.Char(string="Retur Pembelian Barang Sufiks")

    terima_brg_prefiks = fields.Char(string="Penerimaan Barang Prefiks")
    terima_brg_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Penerimaan Barang Digit",
        default="3",
    )
    terima_brg_sufiks = fields.Char(string="Penerimaan Barang Sufiks")

    adj_inv_prefiks = fields.Char(string="Adjustment Inventory Prefiks")
    adj_inv_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Adjustment Inventory Digit",
        default="3",
    )
    adj_inv_sufiks = fields.Char(string="Adjustment Inventory Sufiks")

    # Line 4
    tf_brg_prefiks = fields.Char(string="Transfer Barang Prefiks")
    tf_brg_digit = fields.Selection(
        [("3", "3 Digit"), ("4", "4 Digit"), ("5", "5 Digit"), ("6", "6 Digit")],
        string="Transfer Barang Digit",
        default="3",
    )
    tf_brg_sufiks = fields.Char(string="Transfer Barang Sufiks")

    _sql_constraints = [
        ("periode_unique", "unique(periode)", "Periode (yyyymm) harus unik!")
    ]
