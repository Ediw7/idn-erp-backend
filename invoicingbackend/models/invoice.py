from odoo import models, fields, api


class Invoice(models.Model):
    _name = "invoicingbackend.invoice"
    _description = "Faktur Penjualan (Invoice)"
    _inherit = "invoicingbackend.base_tenant"

    no_invoice = fields.Char(string="No. Invoice", required=True, index=True)
    tgl_invoice = fields.Date(
        string="Tgl Invoice", required=True, default=fields.Date.context_today
    )

    pelanggan_id = fields.Many2one(
        "invoicingbackend.pelanggan", string="Pelanggan", required=True
    )
    alamat = fields.Text(string="Alamat", related="pelanggan_id.alamat", readonly=True)

    surat_jalan_id = fields.Many2one(
        "invoicingbackend.surat_jalan", string="Dari Surat Jalan (Legacy)"
    )
    surat_jalan_ids = fields.One2many(
        "invoicingbackend.surat_jalan", "invoice_id", string="Surat Jalan Terkait"
    )
    sales_order_id = fields.Many2one(
        "invoicingbackend.sales_order", string="Dari Sales Order", ondelete="restrict"
    )

    no_fp = fields.Char(string="No. Faktur Pajak")
    tgl_fp = fields.Date(string="Tgl Faktur Pajak")

    keterangan = fields.Text(string="Keterangan")

    # Keuangan
    subtotal = fields.Float(string="Sub Total", compute="_compute_totals", store=True)
    potongan_harga = fields.Float(string="Potongan Harga", default=0.0)
    ppn_persen = fields.Float(string="PPN (%)", default=11.0)
    ppn_amount = fields.Float(
        string="PPN Amount", compute="_compute_totals", store=True
    )
    pph_persen = fields.Float(string="PPh 22 (%)", default=0.0)
    pph_amount = fields.Float(
        string="PPh 22 Amount", compute="_compute_totals", store=True
    )
    ongkos_angkut = fields.Float(string="Ongkos Angkut", default=0.0)
    total = fields.Float(string="Total Tagihan", compute="_compute_totals", store=True)

    # Saldo
    total_terbayar = fields.Float(
        string="Total Terbayar", compute="_compute_terbayar", store=True
    )
    saldo_piutang = fields.Float(
        string="Saldo Piutang", compute="_compute_saldo", store=True
    )

    is_lunas = fields.Boolean(string="Lunas", compute="_compute_saldo", store=True)
    is_void = fields.Boolean(string="Void", default=False)

    line_ids = fields.One2many(
        "invoicingbackend.invoice_line", "invoice_id", string="Detail Invoice"
    )

    def unlink(self):
        for record in self:
            kwitansi_count = self.env['invoicingbackend.kwitansi'].search_count([('invoice_id', '=', record.id)])
            if kwitansi_count > 0:
                raise models.ValidationError("Tidak bisa menghapus Invoice yang sudah memiliki pembayaran/kwitansi.")
        return super(Invoice, self).unlink()

    def write(self, vals):
        if vals.get('is_void'):
            for record in self:
                kwitansi_count = self.env['invoicingbackend.kwitansi'].search_count([('invoice_id', '=', record.id)])
                if kwitansi_count > 0:
                    raise models.ValidationError("Tidak bisa membatalkan (Void) Invoice yang sudah memiliki pembayaran/kwitansi.")
        return super(Invoice, self).write(vals)
    pembayaran_line_ids = fields.One2many(
        "invoicingbackend.pembayaran_piutang_line",
        "invoice_id",
        string="Histori Pembayaran",
    )
    kwitansi_ids = fields.One2many(
        "invoicingbackend.kwitansi",
        "invoice_id",
        string="Histori Kwitansi",
    )

    @api.depends(
        "line_ids.harga_jual",
        "potongan_harga",
        "ppn_persen",
        "pph_persen",
        "ongkos_angkut",
    )
    def _compute_totals(self):
        for record in self:
            sub = sum(line.harga_jual for line in record.line_ids)
            record.subtotal = sub

            dpp = sub - record.potongan_harga
            ppn = dpp * (record.ppn_persen / 100.0)
            record.ppn_amount = ppn

            pph = dpp * (record.pph_persen / 100.0)
            record.pph_amount = pph

            record.total = dpp + ppn + pph + record.ongkos_angkut

    @api.depends(
        "pembayaran_line_ids.pembayaran",
        "pembayaran_line_ids.potongan",
        "pembayaran_line_ids.pembayaran_id.is_void",
        "kwitansi_ids.jumlah",
    )
    def _compute_terbayar(self):
        for record in self:
            # Hanya hitung pembayaran yang valid (tidak void)
            valid_payments = record.pembayaran_line_ids.filtered(
                lambda l: not l.pembayaran_id.is_void
            )
            total_bayar = sum(p.pembayaran + p.potongan for p in valid_payments)
            
            # Hitung juga pembayaran via Kwitansi
            total_kwitansi = sum(k.jumlah for k in record.kwitansi_ids)
            
            record.total_terbayar = total_bayar + total_kwitansi

    @api.depends("total", "total_terbayar")
    def _compute_saldo(self):
        for record in self:
            saldo = record.total - record.total_terbayar
            # Hindari minus kecil akibat pembulatan
            record.saldo_piutang = saldo if saldo > 0.01 else 0.0
            record.is_lunas = record.saldo_piutang <= 0.01


class InvoiceLine(models.Model):
    _name = "invoicingbackend.invoice_line"
    _description = "Invoice Line"
    _inherit = "invoicingbackend.base_tenant"

    invoice_id = fields.Many2one(
        "invoicingbackend.invoice", string="Invoice", ondelete="cascade"
    )
    item_id = fields.Many2one("invoicingbackend.item", string="Item", required=True)
    nama_barang = fields.Char(
        related="item_id.nama", string="Nama Barang", readonly=True
    )
    satuan = fields.Char(string="Satuan")

    kuantum = fields.Float(string="Kuantum", default=1.0)
    harga_satuan = fields.Float(string="Harga Satuan")
    disc_persen = fields.Float(string="% Disc", default=0.0)
    disc_harga = fields.Float(string="Disc Harga", default=0.0)

    harga_jual = fields.Float(
        string="Subtotal Line", compute="_compute_harga_jual", store=True
    )

    @api.depends("kuantum", "harga_satuan", "disc_persen", "disc_harga")
    def _compute_harga_jual(self):
        for line in self:
            base_price = line.kuantum * line.harga_satuan
            discount = (base_price * (line.disc_persen / 100.0)) + line.disc_harga
            line.harga_jual = base_price - discount

    @api.constrains("kuantum", "harga_satuan", "disc_persen", "disc_harga")
    def _check_negative_values(self):
        for line in self:
            if (
                line.kuantum < 0
                or line.harga_satuan < 0
                or line.disc_persen < 0
                or line.disc_harga < 0
            ):
                raise models.ValidationError(
                    "Kuantum, harga satuan, dan diskon tidak boleh bernilai negatif."
                )
