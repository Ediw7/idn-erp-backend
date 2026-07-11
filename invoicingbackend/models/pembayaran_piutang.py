from odoo import models, fields, api


class PembayaranPiutang(models.Model):
    _name = "invoicingbackend.pembayaran_piutang"
    _description = "Bukti Pembayaran Piutang"
    _inherit = "invoicingbackend.base_tenant"

    no_bukti = fields.Char(string="No. Bukti", required=True, index=True)
    tgl_pembayaran = fields.Date(
        string="Tgl Pembayaran", required=True, default=fields.Date.context_today
    )

    pelanggan_id = fields.Many2one(
        "invoicingbackend.pelanggan", string="Dibayar Oleh", required=True
    )

    perkiraan_kas_id = fields.Many2one(
        "invoicingbackend.perkiraan", string="Kas/Bank Penerima"
    )
    keterangan = fields.Text(string="Keterangan")

    total_pembayaran = fields.Float(
        string="Total Pembayaran", compute="_compute_totals", store=True
    )
    total_potongan = fields.Float(
        string="Total Potongan", compute="_compute_totals", store=True
    )

    is_void = fields.Boolean(string="Void", default=False)

    line_ids = fields.One2many(
        "invoicingbackend.pembayaran_piutang_line",
        "pembayaran_id",
        string="Rincian Pembayaran",
    )

    @api.depends("line_ids.pembayaran", "line_ids.potongan")
    def _compute_totals(self):
        for record in self:
            record.total_pembayaran = sum(line.pembayaran for line in record.line_ids)
            record.total_potongan = sum(line.potongan for line in record.line_ids)


class PembayaranPiutangLine(models.Model):
    _name = "invoicingbackend.pembayaran_piutang_line"
    _description = "Rincian Pembayaran Piutang"
    _inherit = "invoicingbackend.base_tenant"

    pembayaran_id = fields.Many2one(
        "invoicingbackend.pembayaran_piutang",
        string="Bukti Pembayaran",
        ondelete="cascade",
    )
    invoice_id = fields.Many2one(
        "invoicingbackend.invoice", string="Invoice", required=True, ondelete="restrict"
    )

    saldo_piutang = fields.Float(
        related="invoice_id.total", string="Total Tagihan Awal", readonly=True
    )
    pembayaran = fields.Float(string="Nilai Pembayaran", required=True, default=0.0)
    potongan = fields.Float(string="Nilai Potongan", default=0.0)

    # Perkiraan untuk potongan (misal: beban diskon/potongan pembayaran)
    perkiraan_potongan_id = fields.Many2one(
        "invoicingbackend.perkiraan", string="Perkiraan Potongan"
    )
    keterangan = fields.Char(string="Keterangan")

    @api.constrains("pembayaran", "potongan", "invoice_id")
    def _check_overpayment(self):
        for line in self:
            if line.pembayaran < 0 or line.potongan < 0:
                raise models.ValidationError(
                    "Pembayaran dan potongan tidak boleh bernilai negatif."
                )

            # Cari seluruh pembayaran untuk invoice ini, KECUALI pembayaran dari record yang sedang void
            # Kita gunakan sudo() atau search() untuk menjumlahkan semua.
            all_payments = self.env["invoicingbackend.pembayaran_piutang_line"].search(
                [
                    ("invoice_id", "=", line.invoice_id.id),
                    ("pembayaran_id.is_void", "=", False),
                    ("id", "!=", line.id if line.id else False),
                ]
            )
            total_paid_others = sum(p.pembayaran + p.potongan for p in all_payments)
            total_attempted = total_paid_others + line.pembayaran + line.potongan

            if total_attempted > line.invoice_id.total + 0.01:
                raise models.ValidationError(
                    f"Overpayment! Total pembayaran dan potongan yang dicoba ({total_attempted}) melebihi total tagihan Invoice ({line.invoice_id.total})."
                )
