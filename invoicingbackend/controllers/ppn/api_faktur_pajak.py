import json
from datetime import datetime
import logging
from odoo import http
from odoo.http import request

try:
    from ..api_response import success_response, error_response
except ImportError:
    try:
        from ..utils import success_response, error_response
    except ImportError:

        def success_response(message="Success", data=None, meta=None):
            resp = {"status": "success", "message": message}
            if data is not None:
                resp["data"] = data
            if meta is not None:
                resp["meta"] = meta
            return request.make_response(
                json.dumps(resp), headers=[("Content-Type", "application/json")]
            )

        def error_response(message="Error", status=400):
            resp = {"status": "error", "message": message}
            return request.make_response(
                json.dumps(resp),
                status=status,
                headers=[("Content-Type", "application/json")],
            )


_logger = logging.getLogger(__name__)


class ApiFakturPajak(http.Controller):

    @http.route(
        "/api/faktur_pajak",
        type="http",
        auth="user",
        methods=["GET", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def get_faktur_pajak(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        try:
            domain = []

            page = int(kwargs.get("page", 1))
            limit = int(kwargs.get("limit", 100))
            offset = (page - 1) * limit

            periode = kwargs.get("periode")
            if periode:
                year = periode[:4]
                month = periode[4:]
                start_date = f"{year}-{month}-01"
                end_date = (
                    f"{year}-{month}-31"
                    if month in ["01", "03", "05", "07", "08", "10", "12"]
                    else f"{year}-{month}-30"
                )
                if month == "02":
                    end_date = (
                        f"{year}-{month}-29"
                        if int(year) % 4 == 0
                        else f"{year}-{month}-28"
                    )
                domain.append(("tgl_fp", ">=", start_date))
                domain.append(("tgl_fp", "<=", end_date))

            search = kwargs.get("search")
            if search:
                domain.append("|")
                domain.append(("no_fp", "ilike", search))
                domain.append(("pembeli_id.nama", "ilike", search))

            records = request.env["invoicingbackend.transaksi_faktur_pajak"].search(
                domain, order="tgl_fp desc, id desc", limit=limit, offset=offset
            )
            total_count = request.env[
                "invoicingbackend.transaksi_faktur_pajak"
            ].search_count(domain)

            data = []
            for rec in records:
                lines = []
                for line in rec.line_ids:
                    lines.append(
                        {
                            "id": line.id,
                            "item_id": line.item_id.id if line.item_id else None,
                            "kode_barang": line.item_id.kode if line.item_id else "",
                            "nama_barang": line.item_id.nama if line.item_id else "",
                            "satuan": line.item_id.satuan if line.item_id else "Pcs",
                            "kuantum": line.kuantum,
                            "harga_satuan": line.harga_satuan,
                            "harga_jual": line.harga_jual,
                        }
                    )

                data.append(
                    {
                        "id": rec.id,
                        "penomoran": rec.penomoran or "",
                        "no_fp": rec.no_fp or "",
                        "tgl_fp": rec.tgl_fp.strftime("%Y-%m-%d") if rec.tgl_fp else "",
                        "pembeli_id": rec.pembeli_id.id if rec.pembeli_id else None,
                        "pembeli_nama": rec.pembeli_id.nama if rec.pembeli_id else "",
                        "pembeli_npwp": rec.pembeli_id.npwp if rec.pembeli_id else "",
                        "alamat": rec.pembeli_id.alamat_wp
                        or rec.pembeli_id.alamat
                        or "",
                        "npwp": rec.pembeli_id.npwp or "",
                        "fp_diganti": rec.fp_diganti or "",
                        "tgl_fp_diganti": (
                            rec.tgl_fp_diganti.strftime("%Y-%m-%d")
                            if rec.tgl_fp_diganti
                            else ""
                        ),
                        "jenis_transaksi": rec.jenis_transaksi or "",
                        "jenis_status": rec.jenis_status or "",
                        "no_invoice": rec.no_invoice or "",
                        "tarif_ppn": rec.tarif_ppn,
                        "mata_uang": rec.mata_uang or "IDR",
                        "kurs_pajak": rec.kurs_pajak,
                        "penandatangan": rec.penandatangan or "",
                        "jabatan": rec.jabatan or "",
                        "ket_tambahan": rec.ket_tambahan or "",
                        "potongan": rec.potongan,
                        "uang_muka": rec.uang_muka,
                        "dpp_rp": rec.dpp_rp,
                        "ppn_rp": rec.ppn_rp,
                        "lines": lines,
                    }
                )

            return success_response(
                message="Data Faktur Pajak berhasil diambil",
                data=data,
                meta={
                    "pagination": {
                        "total": total_count,
                        "page": page,
                        "limit": limit,
                        "last_page": (total_count + limit - 1) // limit,
                    }
                },
            )
        except Exception as e:
            _logger.error("Error in get_faktur_pajak: %s", str(e))
            return error_response(str(e))

    @http.route(
        "/api/faktur_pajak/<int:id>",
        type="http",
        auth="user",
        methods=["GET", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def get_faktur_pajak_by_id(self, id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        try:
            rec = request.env["invoicingbackend.transaksi_faktur_pajak"].browse(id)
            if not rec.exists():
                return error_response("Data tidak ditemukan", status=404)

            lines = []
            for line in rec.line_ids:
                lines.append(
                    {
                        "id": line.id,
                        "item_id": line.item_id.id if line.item_id else None,
                        "kode_barang": line.item_id.kode if line.item_id else "",
                        "nama_barang": line.item_id.nama if line.item_id else "",
                        "satuan": line.item_id.satuan if line.item_id else "Pcs",
                        "kuantum": line.kuantum,
                        "harga_satuan": line.harga_satuan,
                        "harga_jual": line.harga_jual,
                    }
                )

            data = {
                "id": rec.id,
                "penomoran": rec.penomoran or "",
                "no_fp": rec.no_fp or "",
                "tgl_fp": rec.tgl_fp.strftime("%Y-%m-%d") if rec.tgl_fp else "",
                "pembeli_id": rec.pembeli_id.id if rec.pembeli_id else None,
                "pembeli_nama": rec.pembeli_id.nama if rec.pembeli_id else "",
                "pembeli_npwp": rec.pembeli_id.npwp if rec.pembeli_id else "",
                "alamat": rec.pembeli_id.alamat_wp or rec.pembeli_id.alamat or "",
                "npwp": rec.pembeli_id.npwp or "",
                "fp_diganti": rec.fp_diganti or "",
                "tgl_fp_diganti": (
                    rec.tgl_fp_diganti.strftime("%Y-%m-%d")
                    if rec.tgl_fp_diganti
                    else ""
                ),
                "jenis_transaksi": rec.jenis_transaksi or "",
                "jenis_status": rec.jenis_status or "",
                "no_invoice": rec.no_invoice or "",
                "tarif_ppn": rec.tarif_ppn,
                "mata_uang": rec.mata_uang or "IDR",
                "kurs_pajak": rec.kurs_pajak,
                "penandatangan": rec.penandatangan or "",
                "jabatan": rec.jabatan or "",
                "ket_tambahan": rec.ket_tambahan or "",
                "potongan": rec.potongan,
                "uang_muka": rec.uang_muka,
                "dpp_rp": rec.dpp_rp,
                "ppn_rp": rec.ppn_rp,
                "lines": lines,
            }

            return success_response("Data berhasil diambil", data)
        except Exception as e:
            _logger.error("Error get_faktur_pajak_by_id: %s", str(e))
            return error_response(str(e))

    @http.route(
        "/api/faktur_pajak",
        type="http",
        auth="user",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def create_faktur_pajak(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        try:
            payload = json.loads(request.httprequest.data.decode("utf-8"))

            vals = {
                "penomoran": payload.get("penomoran"),
                "no_fp": payload.get("no_fp"),
                "pembeli_id": payload.get("pembeli_id"),
                "fp_diganti": payload.get("fp_diganti"),
                "jenis_transaksi": payload.get("jenis_transaksi"),
                "jenis_status": payload.get("jenis_status"),
                "no_invoice": payload.get("no_invoice"),
                "tarif_ppn": payload.get("tarif_ppn", 11),
                "mata_uang": payload.get("mata_uang", "IDR"),
                "kurs_pajak": payload.get("kurs_pajak", 1),
                "penandatangan": payload.get("penandatangan"),
                "jabatan": payload.get("jabatan"),
                "ket_tambahan": payload.get("ket_tambahan"),
                "potongan": payload.get("potongan", 0),
                "uang_muka": payload.get("uang_muka", 0),
                "dpp_rp": payload.get("dpp_rp", 0),
                "ppn_rp": payload.get("ppn_rp", 0),
            }

            if payload.get("tgl_fp"):
                vals["tgl_fp"] = payload.get("tgl_fp")
            if payload.get("tgl_fp_diganti"):
                vals["tgl_fp_diganti"] = payload.get("tgl_fp_diganti")

            rec = request.env["invoicingbackend.transaksi_faktur_pajak"].create(vals)

            lines_data = payload.get("lines", [])
            for line_data in lines_data:
                request.env["invoicingbackend.transaksi_faktur_pajak_line"].create(
                    {
                        "faktur_id": rec.id,
                        "item_id": line_data.get("item_id"),
                        "kuantum": line_data.get("kuantum", 0),
                        "harga_satuan": line_data.get("harga_satuan", 0),
                        "harga_jual": line_data.get("harga_jual", 0),
                    }
                )

            return success_response("Berhasil dibuat", {"id": rec.id})
        except Exception as e:
            _logger.error("Error create_faktur_pajak: %s", str(e))
            return error_response(str(e))

    @http.route(
        "/api/faktur_pajak/<int:id>",
        type="http",
        auth="user",
        methods=["PUT", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def update_faktur_pajak(self, id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        try:
            rec = request.env["invoicingbackend.transaksi_faktur_pajak"].browse(id)
            if not rec.exists():
                return error_response("Data tidak ditemukan", status=404)

            payload = json.loads(request.httprequest.data.decode("utf-8"))

            vals = {
                "penomoran": payload.get("penomoran"),
                "no_fp": payload.get("no_fp"),
                "pembeli_id": payload.get("pembeli_id"),
                "fp_diganti": payload.get("fp_diganti"),
                "jenis_transaksi": payload.get("jenis_transaksi"),
                "jenis_status": payload.get("jenis_status"),
                "no_invoice": payload.get("no_invoice"),
                "tarif_ppn": payload.get("tarif_ppn", 11),
                "mata_uang": payload.get("mata_uang", "IDR"),
                "kurs_pajak": payload.get("kurs_pajak", 1),
                "penandatangan": payload.get("penandatangan"),
                "jabatan": payload.get("jabatan"),
                "ket_tambahan": payload.get("ket_tambahan"),
                "potongan": payload.get("potongan", 0),
                "uang_muka": payload.get("uang_muka", 0),
                "dpp_rp": payload.get("dpp_rp", 0),
                "ppn_rp": payload.get("ppn_rp", 0),
            }

            if payload.get("tgl_fp"):
                vals["tgl_fp"] = payload.get("tgl_fp")
            if payload.get("tgl_fp_diganti"):
                vals["tgl_fp_diganti"] = payload.get("tgl_fp_diganti")

            rec.write(vals)

            lines_data = payload.get("lines", [])
            existing_line_ids = rec.line_ids.ids
            new_line_ids = []

            for line_data in lines_data:
                line_vals = {
                    "faktur_id": rec.id,
                    "item_id": line_data.get("item_id"),
                    "kuantum": line_data.get("kuantum", 0),
                    "harga_satuan": line_data.get("harga_satuan", 0),
                    "harga_jual": line_data.get("harga_jual", 0),
                }

                line_id = line_data.get("id")
                if line_id and line_id in existing_line_ids:
                    request.env["invoicingbackend.transaksi_faktur_pajak_line"].browse(
                        line_id
                    ).write(line_vals)
                    new_line_ids.append(line_id)
                else:
                    new_line = request.env[
                        "invoicingbackend.transaksi_faktur_pajak_line"
                    ].create(line_vals)
                    new_line_ids.append(new_line.id)

            lines_to_delete = set(existing_line_ids) - set(new_line_ids)
            if lines_to_delete:
                request.env["invoicingbackend.transaksi_faktur_pajak_line"].browse(
                    list(lines_to_delete)
                ).unlink()

            return success_response("Berhasil diperbarui", {"id": rec.id})
        except Exception as e:
            _logger.error("Error update_faktur_pajak: %s", str(e))
            return error_response(str(e))

    @http.route(
        "/api/faktur_pajak/<int:id>",
        type="http",
        auth="user",
        methods=["DELETE", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def delete_faktur_pajak_by_id(self, id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        try:
            rec = request.env["invoicingbackend.transaksi_faktur_pajak"].browse(id)
            if rec.exists():
                rec.unlink()
            return success_response("Berhasil dihapus")
        except Exception as e:
            _logger.error("Error delete_faktur_pajak: %s", str(e))
            return error_response(str(e))
