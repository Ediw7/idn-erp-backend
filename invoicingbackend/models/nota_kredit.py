from odoo import models, fields, api

class NotaKredit(models.Model):
    _name = "invoicingbackend.nota_kredit"
    _description = "Nota Kredit (Credit Note)"
    _inherit = "invoicingbackend.base_tenant"

    no_nota_kredit = fields.Char(string="No. Nota Kredit", required=True, index=True)
    tgl_nota_kredit = fields.Date(
        string="Tanggal Nota Kredit", required=True, default=fields.Date.today, index=True
    )
    periode = fields.Char(string="Periode (yyyymm)")

    pelanggan_id = fields.Many2one(
        "invoicingbackend.pelanggan", string="Pelanggan", required=True, index=True
    )
    alamat = fields.Text(string="Alamat", related="pelanggan_id.alamat", readonly=True)

    invoice_id = fields.Many2one(
        "invoicingbackend.invoice", string="Atas No. Invoice", ondelete="restrict", index=True
    )
    no_referensi = fields.Char(string="No. Referensi")

    mata_uang_id = fields.Many2one(
        "invoicingbackend.mata_uang", string="Mata Uang"
    )

    tanda_tangan = fields.Char(string="Tanda Tangan")
    jabatan = fields.Char(string="Jabatan")

    # Lines
    line_ids = fields.One2many(
        "invoicingbackend.nota_kredit_line", "nota_kredit_id", string="Detail Nota Kredit"
    )

    nilai_nota_kredit = fields.Float(
        string="Nilai Nota Kredit", compute="_compute_nilai", store=True
    )

    @api.depends("line_ids.jumlah")
    def _compute_nilai(self):
        for record in self:
            record.nilai_nota_kredit = sum(line.jumlah for line in record.line_ids)


class NotaKreditLine(models.Model):
    _name = "invoicingbackend.nota_kredit_line"
    _description = "Detail Nota Kredit"
    _inherit = "invoicingbackend.base_tenant"

    nota_kredit_id = fields.Many2one(
        "invoicingbackend.nota_kredit", string="Nota Kredit", ondelete="cascade"
    )
    keterangan = fields.Char(string="Keterangan", required=True)
    jumlah = fields.Float(string="Jumlah", required=True)
    no_perkiraan = fields.Char(string="No Perkiraan")

    @api.constrains("jumlah")
    def _check_jumlah(self):
        for line in self:
            if line.jumlah < 0:
                raise models.ValidationError("Jumlah tidak boleh negatif.")
