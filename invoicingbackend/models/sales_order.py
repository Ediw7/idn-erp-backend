from odoo import models, fields, api


class SalesOrder(models.Model):
    _name = "invoicingbackend.sales_order"
    _description = "Sales Order"
    _inherit = "invoicingbackend.base_tenant"

    no_so = fields.Char(string="No. Sales Order", required=True)
    tgl_so = fields.Date(
        string="Tgl Sales Order", required=True, default=fields.Date.context_today
    )
    pelanggan_id = fields.Many2one(
        "invoicingbackend.pelanggan", string="Pelanggan", required=True
    )
    alamat_kirim = fields.Text(string="Dikirim ke Alamat")

    no_po = fields.Char(string="No. PO Pelanggan")
    tgl_po = fields.Date(string="Tgl PO")
    mata_uang_id = fields.Many2one("invoicingbackend.mata_uang", string="Mata Uang")
    pembayaran_id = fields.Many2one(
        "invoicingbackend.pembayaran", string="Cara Pembayaran"
    )
    salesman_id = fields.Many2one("invoicingbackend.salesman", string="Salesman")
    tgl_kirim = fields.Date(string="Tgl Kirim")
    dipesan_oleh = fields.Char(string="Dipesan Oleh")

    is_closed = fields.Boolean(
        string="Closed", compute="_compute_is_closed", store=True
    )
    is_void = fields.Boolean(string="Void", default=False)

    keterangan = fields.Text(string="Keterangan")

    invoice_ids = fields.One2many(
        "invoicingbackend.invoice", "sales_order_id", string="Invoices"
    )

    subtotal = fields.Float(string="Sub Total", compute="_compute_totals", store=True)
    potongan_harga = fields.Float(string="Potongan Harga")
    ppn_persen = fields.Float(string="PPN (%)", default=10.0)
    ppn_amount = fields.Float(
        string="PPN Amount", compute="_compute_totals", store=True
    )
    ppnbm_persen = fields.Float(string="PPnBM (%)", default=0.0)
    ppnbm_amount = fields.Float(
        string="PPnBM Amount", compute="_compute_totals", store=True
    )
    ongkos_angkut = fields.Float(string="Ongkos Angkut")
    total = fields.Float(string="Total", compute="_compute_totals", store=True)

    line_ids = fields.One2many(
        "invoicingbackend.sales_order_line", "so_id", string="Detail Barang/Jasa"
    )

    @api.depends(
        "line_ids.harga_jual",
        "potongan_harga",
        "ppn_persen",
        "ppnbm_persen",
        "ongkos_angkut",
    )
    def _compute_totals(self):
        for record in self:
            subtotal = sum(line.harga_jual for line in record.line_ids)
            record.subtotal = subtotal

            dpp = subtotal - record.potongan_harga
            ppn_amt = dpp * (record.ppn_persen / 100.0)
            ppnbm_amt = dpp * (record.ppnbm_persen / 100.0)
            record.ppn_amount = ppn_amt
            record.ppnbm_amount = ppnbm_amt

            record.total = dpp + ppn_amt + ppnbm_amt + record.ongkos_angkut

    @api.depends("invoice_ids.is_lunas", "invoice_ids.is_void")
    def _compute_is_closed(self):
        for record in self:
            valid_invoices = record.invoice_ids.filtered(lambda inv: not inv.is_void)
            if valid_invoices:
                # Jika ada invoice yang valid, SO dianggap tertutup jika semuanya lunas
                record.is_closed = all(inv.is_lunas for inv in valid_invoices)
            else:
                record.is_closed = False

    def unlink(self):
        for record in self:
            sj_count = self.env['invoicingbackend.surat_jalan'].search_count([('so_id', '=', record.id)])
            if sj_count > 0:
                raise models.ValidationError("Tidak bisa menghapus Sales Order yang sudah memiliki Surat Jalan terkait.")
            if record.invoice_ids:
                raise models.ValidationError("Tidak bisa menghapus Sales Order yang sudah memiliki Tagihan (Invoice) terkait.")
        return super(SalesOrder, self).unlink()

    def write(self, vals):
        if vals.get('is_void'):
            for record in self:
                sj_count = self.env['invoicingbackend.surat_jalan'].search_count([('so_id', '=', record.id)])
                if sj_count > 0:
                    raise models.ValidationError("Tidak bisa membatalkan (Void) Sales Order yang sudah memiliki Surat Jalan terkait.")
                if record.invoice_ids:
                    raise models.ValidationError("Tidak bisa membatalkan (Void) Sales Order yang sudah memiliki Tagihan (Invoice) terkait.")
        return super(SalesOrder, self).write(vals)


class SalesOrderLine(models.Model):
    _name = "invoicingbackend.sales_order_line"
    _description = "Sales Order Line"
    _inherit = "invoicingbackend.base_tenant"

    so_id = fields.Many2one(
        "invoicingbackend.sales_order", string="Sales Order", ondelete="cascade"
    )
    item_id = fields.Many2one(
        "invoicingbackend.item", string="Kode Barang", required=True
    )
    nama_barang = fields.Char(
        related="item_id.nama", string="Nama Barang", readonly=True
    )
    satuan = fields.Char(string="Satuan")
    kuantum = fields.Float(string="Kuantum", default=1.0)
    harga_satuan = fields.Float(string="Harga Satuan")
    disc_persen = fields.Float(string="% Disc")
    disc_harga = fields.Float(string="Discount Harga")
    harga_jual = fields.Float(
        string="Harga Jual", compute="_compute_harga_jual", store=True
    )
    keterangan = fields.Char(string="Keterangan")

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
