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

            # Di environment production, ini akan memanggil engine wkhtmltopdf Odoo:
            # pdf_content, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf('module.report_id', res_ids)

            # Fallback: Buat PDF valid yang sangat sederhana (Minimal PDF Spec)
            # Ini memastikan frontend tidak error saat 파parsing Blob PDF
            minimal_pdf = (
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

            return request.make_response(minimal_pdf, headers=headers)

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
