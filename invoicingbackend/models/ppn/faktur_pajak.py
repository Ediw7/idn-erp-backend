from odoo import models, fields, api


class FakturPajak(models.Model):
    _name = "invoicingbackend.transaksi_faktur_pajak"
    _description = "Transaksi Faktur Pajak"
    _inherit = "invoicingbackend.base_tenant"

    penomoran = fields.Char(string="Penomoran NSFP")
    no_fp = fields.Char(string="No. Faktur Pajak", required=True)
    tgl_fp = fields.Date(string="Tgl. Faktur Pajak", required=True)

    pembeli_id = fields.Many2one("invoicingbackend.pelanggan", string="Pembeli")

    fp_diganti = fields.Char(string="Faktur Pajak Diganti")
    tgl_fp_diganti = fields.Date(string="Tgl FP Diganti")

    jenis_transaksi = fields.Char(
        string="Jenis Transaksi", default="01 - Kepada Bukan Pemungut PPN"
    )
    jenis_status = fields.Char(string="Jenis Status", default="Normal")

    no_invoice = fields.Char(string="No. Invoice")

    tarif_ppn = fields.Float(string="Tarif PPN (%)", default=11.0)
    mata_uang = fields.Char(string="Mata Uang", default="IDR")
    kurs_pajak = fields.Float(string="Kurs Pajak", default=1.0)

    penandatangan = fields.Char(string="Penandatangan")
    jabatan = fields.Char(string="Jabatan")
    ket_tambahan = fields.Text(string="Keterangan Tambahan")

    potongan = fields.Float(string="Potongan")
    uang_muka = fields.Float(string="Uang Muka")

    dpp_rp = fields.Float(string="DPP (Rp)")
    ppn_rp = fields.Float(string="PPN (Rp)")

    line_ids = fields.One2many(
        "invoicingbackend.transaksi_faktur_pajak_line",
        "faktur_id",
        string="Detail Barang",
    )


class FakturPajakLine(models.Model):
    _name = "invoicingbackend.transaksi_faktur_pajak_line"
    _description = "Detail Faktur Pajak"
    _inherit = "invoicingbackend.base_tenant"

    faktur_id = fields.Many2one(
        "invoicingbackend.transaksi_faktur_pajak",
        string="Faktur Pajak",
        ondelete="cascade",
    )
    item_id = fields.Many2one("invoicingbackend.item", string="Barang")

    kuantum = fields.Float(string="Kuantum", default=1.0)
    harga_satuan = fields.Float(string="Harga Satuan")
    harga_jual = fields.Float(string="Harga Jual (DPP)")
