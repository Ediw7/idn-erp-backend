import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ApiKartuPiutang(http.Controller):

    @http.route(
        "/api/piutang/kartu",
        type="http",
        auth="user",
        methods=["GET", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def get_kartu_piutang(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        pelanggan_id = kwargs.get("pelanggan_id")
        mata_uang = kwargs.get("mata_uang", "IDR")

        if not pelanggan_id:
            return self.error_response("pelanggan_id is required")

        try:
            pelanggan_id = int(pelanggan_id)
        except ValueError:
            return self.error_response("Invalid pelanggan_id format")

        try:
            riwayat_list = []

            # 1. Ambil dari Invoice (Debit)
            invoices = request.env["invoicingbackend.invoice"].sudo().search([
                ("pelanggan_id", "=", pelanggan_id)
            ])
            for inv in invoices:
                # Mata uang check if needed
                # Here we assume all invoices are fetched, you might filter by currency later
                riwayat_list.append({
                    "id": f"inv_{inv.id}",
                    "tanggal": str(inv.tanggal_faktur) if inv.tanggal_faktur else "",
                    "no_invoice": inv.no_invoice or "",
                    "no_ref": inv.po_nomor or "",
                    "keterangan": inv.keterangan or "Penjualan (Invoice)",
                    "debet": inv.total or 0.0,
                    "kredit": 0.0,
                })

            # 2. Ambil dari Pembayaran Piutang (Kredit)
            pembayaran_lines = request.env["invoicingbackend.pembayaran_piutang_line"].sudo().search([
                ("pembayaran_id.pelanggan_id", "=", pelanggan_id),
                ("pembayaran_id.is_void", "=", False)
            ])
            for line in pembayaran_lines:
                total_kredit = (line.pembayaran or 0.0) + (line.potongan or 0.0)
                riwayat_list.append({
                    "id": f"pay_{line.id}",
                    "tanggal": str(line.pembayaran_id.tgl_pembayaran) if line.pembayaran_id.tgl_pembayaran else "",
                    "no_invoice": line.invoice_id.no_invoice if line.invoice_id else "",
                    "no_ref": line.pembayaran_id.no_bukti or "",
                    "keterangan": line.keterangan or line.pembayaran_id.keterangan or "Pembayaran Piutang",
                    "debet": 0.0,
                    "kredit": total_kredit,
                })

            # 3. Ambil dari Nota Kredit (Kredit)
            nota_kredits = request.env["invoicingbackend.nota_kredit"].sudo().search([
                ("pelanggan_id", "=", pelanggan_id)
            ])
            for nk in nota_kredits:
                riwayat_list.append({
                    "id": f"nk_{nk.id}",
                    "tanggal": str(nk.tgl_nota_kredit) if nk.tgl_nota_kredit else "",
                    "no_invoice": nk.invoice_id.no_invoice if nk.invoice_id else "",
                    "no_ref": nk.no_nota_kredit or "",
                    "keterangan": "Nota Kredit",
                    "debet": 0.0,
                    "kredit": nk.nilai_nota_kredit or 0.0,
                })

            # Sort by tanggal
            # Sort by tanggal ascending. If tanggal is empty, put it first (or last)
            riwayat_list.sort(key=lambda x: x["tanggal"])

            resp = {
                "status": "success",
                "data": riwayat_list
            }
            return request.make_response(json.dumps(resp), headers=[("Content-Type", "application/json")])

        except Exception as e:
            _logger.error(f"Error getting kartu piutang: {str(e)}")
            return self.error_response(str(e))

    def error_response(self, message="Error", status=400):
        resp = {"status": "error", "message": message}
        return request.make_response(
            json.dumps(resp),
            status=status,
            headers=[("Content-Type", "application/json")],
        )
