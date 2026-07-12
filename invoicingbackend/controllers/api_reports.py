import json
import logging
import io
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ApiReports(http.Controller):

    @http.route(
        "/api/reports/generate",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def generate_report(self, **kw):
        try:
            # Karena Axios POST mengirim raw JSON body
            payload_data = request.httprequest.data.decode("utf-8")
            if payload_data:
                payload = json.loads(payload_data)
            else:
                payload = {}

            report_type = payload.get("reportType", "Unknown")
            filters = payload.get("filters", {})

            _logger.info(f"Generating PDF for: {report_type} | Filters: {filters}")

            if str(report_type).startswith("inv_"):
                no_invoice = filters.get("dari_no_invoice")
                if not no_invoice:
                    raise ValueError(
                        "Nomor Invoice (dari_no_invoice) tidak ditemukan di filter"
                    )

                invoice_id = (
                    request.env["invoicingbackend.invoice"]
                    .sudo()
                    .search([("no_invoice", "=", no_invoice)], limit=1)
                    .id
                )

                if not invoice_id:
                    raise ValueError(
                        f"Invoice dengan nomor {no_invoice} tidak ditemukan di database"
                    )

                pdf_content, _ = (
                    request.env["ir.actions.report"]
                    .sudo()
                    ._render_qweb_pdf(
                        "invoicingbackend.action_report_invoice", [invoice_id]
                    )
                )

            elif str(report_type).startswith("sj_"):
                no_sj = filters.get("dari_no_sj")
                if not no_sj:
                    raise ValueError(
                        "Nomor Surat Jalan (dari_no_sj) tidak ditemukan di filter"
                    )

                sj_id = (
                    request.env["invoicingbackend.surat_jalan"]
                    .sudo()
                    .search([("no_sj", "=", no_sj)], limit=1)
                    .id
                )

                if not sj_id:
                    raise ValueError(
                        f"Surat Jalan dengan nomor {no_sj} tidak ditemukan di database"
                    )

                pdf_content, _ = (
                    request.env["ir.actions.report"]
                    .sudo()
                    ._render_qweb_pdf(
                        "invoicingbackend.action_report_surat_jalan", [sj_id]
                    )
                )

            elif str(report_type).startswith("so_"):
                no_so = filters.get("dari_no_so")
                if not no_so:
                    raise ValueError(
                        "Nomor Sales Order (dari_no_so) tidak ditemukan di filter"
                    )

                so_id = (
                    request.env["invoicingbackend.sales_order"]
                    .sudo()
                    .search([("no_so", "=", no_so)], limit=1)
                    .id
                )

                if not so_id:
                    raise ValueError(
                        f"Sales Order dengan nomor {no_so} tidak ditemukan di database"
                    )

                pdf_content, _ = (
                    request.env["ir.actions.report"]
                    .sudo()
                    ._render_qweb_pdf(
                        "invoicingbackend.action_report_sales_order", [so_id]
                    )
                )

            else:
                # Fallback untuk tipe laporan lain yang belum diimplementasikan
                pdf_content = (
                    b"%PDF-1.4\n"
                    b"1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj\n"
                    b"2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj\n"
                    b"3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources <<>> /Contents 4 0 R>> endobj\n"
                    b"4 0 obj <</Length 53>> stream\n"
                    b"BT\n/F1 24 Tf\n100 700 Td\n(Laporan: "
                    + str(report_type).encode("utf-8")
                    + b") Tj\nET\n"
                    b"endstream endobj\n"
                    b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n0000000212 00000 n\n"
                    b"trailer <</Size 5 /Root 1 0 R>>\n"
                    b"startxref\n314\n"
                    b"%%EOF\n"
                )

            headers = [
                ("Content-Type", "application/pdf"),
                ("Content-Disposition", f'inline; filename="{report_type}.pdf"'),
                ("Access-Control-Allow-Origin", "*"),
            ]

            return request.make_response(pdf_content, headers=headers)
        except Exception as e:
            _logger.error("Error generating report API: %s", str(e))
            return request.make_response(
                json.dumps({"status": "error", "message": str(e)}),
                status=500,
                headers=[("Content-Type", "application/json")],
            )

    # Tangani Preflight OPTIONS request dari Axios (CORS)
    @http.route(
        "/api/reports/generate",
        type="http",
        auth="public",
        methods=["OPTIONS"],
        csrf=False,
    )
    def generate_report_options(self, **kw):
        headers = [
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "POST, OPTIONS"),
            ("Access-Control-Allow-Headers", "Content-Type, Authorization"),
        ]
        return request.make_response("", headers=headers)
