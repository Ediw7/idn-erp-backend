from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
import logging

_logger = logging.getLogger(__name__)


class ApiCekHistoryHargaJual(http.Controller):

    @http.route(
        "/api/history-harga-jual/get",
        type="json",
        auth="user",
        methods=["POST"],
        cors="*",
    )
    def get_history(self, **kwargs):
        try:
            params = request.jsonrequest.get("params", {})

            kode_barang = params.get("kode_barang")
            nama_barang = params.get("nama_barang")
            nama_pelanggan = params.get("nama_pelanggan")
            limit = int(params.get("limit", 25))

            domain = [
                ("invoice_id.company_id", "=", request.env.user.company_id.id),
                ("invoice_id.is_void", "=", False),
            ]

            if kode_barang:
                domain.append(("item_id.kode", "ilike", kode_barang))
            if nama_barang:
                domain.append(("item_id.nama", "ilike", nama_barang))
            if nama_pelanggan:
                domain.append(("invoice_id.pelanggan_id.nama", "ilike", nama_pelanggan))

            # Query the lines, ordered by invoice date descending
            # limit can be 0 or None to mean "Show All"
            line_records = request.env["invoicingbackend.invoice_line"].search(
                domain, order="create_date desc", limit=limit if limit > 0 else None
            )

            data = []
            for line in line_records:
                inv = line.invoice_id

                # Coba dapatkan terms (hari jatuh tempo)
                terms = ""
                if inv.pelanggan_id and inv.pelanggan_id.pembayaran_id:
                    terms = (
                        str(inv.pelanggan_id.pembayaran_id.hari_jatuh_tempo) + " Hari"
                    )

                # Coba dapatkan currency
                curr = "IDR"

                data.append(
                    {
                        "id": line.id,
                        "tgl": str(inv.tgl_invoice) if inv.tgl_invoice else "",
                        "no_invoice": inv.no_invoice or "",
                        "nama_pelanggan": (
                            inv.pelanggan_id.nama if inv.pelanggan_id else ""
                        ),
                        "terms": terms,
                        "curr": curr,
                        "kode_item": line.item_id.kode if line.item_id else "",
                        "nama_item": (
                            line.item_id.nama
                            if line.item_id
                            else line.nama_barang or ""
                        ),
                        "qty": line.kuantum,
                        "harga_satuan": line.harga_satuan,
                        "harga_jual": line.harga_jual,
                    }
                )

            return {"status": "success", "data": data}
        except Exception as e:
            _logger.error(f"Error fetching history: {str(e)}")
            return {"status": "error", "message": str(e)}
