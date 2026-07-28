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

            no_invoice = kwargs.get("no_invoice")
            if no_invoice:
                domain.append(("no_invoice", "=", no_invoice))

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
                            "satuan": line.satuan
                            or (line.item_id.satuan if line.item_id else "Pcs"),
                            "kuantum": line.kuantum,
                            "harga_satuan": line.harga_satuan,
                            "disc_persen": line.disc_persen,
                            "disc_harga": line.disc_harga,
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
                        "satuan": line.satuan
                        or (line.item_id.satuan if line.item_id else "Pcs"),
                        "kuantum": line.kuantum,
                        "harga_satuan": line.harga_satuan,
                        "disc_persen": line.disc_persen,
                        "disc_harga": line.disc_harga,
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
            lines_data = payload.get("lines", [])

            if not lines_data or len(lines_data) == 0:
                return error_response(
                    "Faktur Pajak wajib memiliki minimal 1 barang (lines)."
                )

            if any(
                float(line.get("kuantum", 0)) < 0
                or float(line.get("harga_satuan", 0)) < 0
                for line in lines_data
            ):
                return error_response(
                    "Kuantitas dan Harga Satuan barang tidak boleh minus."
                )

            if (
                float(payload.get("dpp_rp", 0)) < 0
                or float(payload.get("ppn_rp", 0)) < 0
            ):
                return error_response("DPP dan PPN tidak boleh minus.")

            if not payload.get("no_fp"):
                return error_response("Nomor Faktur Pajak (no_fp) wajib diisi.")

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

            for line_data in lines_data:
                request.env["invoicingbackend.transaksi_faktur_pajak_line"].create(
                    {
                        "faktur_id": rec.id,
                        "item_id": line_data.get("item_id"),
                        "satuan": line_data.get("satuan", ""),
                        "kuantum": line_data.get("kuantum", 0),
                        "harga_satuan": line_data.get("harga_satuan", 0),
                        "disc_persen": line_data.get("disc_persen", 0),
                        "disc_harga": line_data.get("disc_harga", 0),
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
            lines_data = payload.get("lines", [])

            if not lines_data or len(lines_data) == 0:
                return error_response(
                    "Faktur Pajak wajib memiliki minimal 1 barang (lines)."
                )

            if any(
                float(line.get("kuantum", 0)) < 0
                or float(line.get("harga_satuan", 0)) < 0
                for line in lines_data
            ):
                return error_response(
                    "Kuantitas dan Harga Satuan barang tidak boleh minus."
                )

            if (
                float(payload.get("dpp_rp", 0)) < 0
                or float(payload.get("ppn_rp", 0)) < 0
            ):
                return error_response("DPP dan PPN tidak boleh minus.")

            if not payload.get("no_fp"):
                return error_response("Nomor Faktur Pajak (no_fp) wajib diisi.")

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

            existing_line_ids = rec.line_ids.ids
            new_line_ids = []

            for line_data in lines_data:
                line_vals = {
                    "faktur_id": rec.id,
                    "item_id": line_data.get("item_id"),
                    "satuan": line_data.get("satuan", ""),
                    "kuantum": line_data.get("kuantum", 0),
                    "harga_satuan": line_data.get("harga_satuan", 0),
                    "disc_persen": line_data.get("disc_persen", 0),
                    "disc_harga": line_data.get("disc_harga", 0),
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

    @http.route(
        "/api/faktur_pajak/auto-no",
        type="http",
        auth="user",
        methods=["POST", "OPTIONS"],
        csrf=False,
        cors="http://localhost:5173",
    )
    def auto_no_fp(self, **kwargs):
        """Generate next No. Faktur Pajak based on selected Penomoran (NSFP range)."""
        if request.httprequest.method == "OPTIONS":
            return http.Response(status=200)

        try:
            payload = json.loads(request.httprequest.data.decode("utf-8"))
            penomoran = payload.get("penomoran", "")
            kode_transaksi = payload.get("kode_transaksi", "01")
            kode_status = payload.get("kode_status", "0")

            if not penomoran:
                return error_response("Penomoran wajib dipilih")

            # Parse range: "000-20.00000001 - 000-20.00099999"
            parts = penomoran.split(" - ")
            if len(parts) != 2:
                return error_response("Format penomoran tidak valid")

            no_seri_awal = parts[0].strip()
            no_seri_akhir = parts[1].strip()

            # Extract numeric part from seri (after last dot)
            # e.g. "000-20.00000001" -> prefix="000-20.", numeric=1
            prefix = ""
            num_start = 0
            num_end = 0

            dot_idx = no_seri_awal.rfind(".")
            if dot_idx >= 0:
                prefix = no_seri_awal[: dot_idx + 1]
                num_start = int(no_seri_awal[dot_idx + 1 :])
                num_end = int(no_seri_akhir[dot_idx + 1 :])
            else:
                # Try extracting trailing digits
                import re

                m = re.match(r"^(.*?)(\d+)$", no_seri_awal)
                if m:
                    prefix = m.group(1)
                    num_start = int(m.group(2))
                    m2 = re.match(r"^(.*?)(\d+)$", no_seri_akhir)
                    num_end = int(m2.group(2)) if m2 else num_start + 99999
                else:
                    return error_response("Format nomor seri tidak valid")

            num_len = len(no_seri_awal) - len(prefix)

            # Find the latest FP using this penomoran
            existing = request.env["invoicingbackend.transaksi_faktur_pajak"].search(
                [("penomoran", "=", penomoran)],
                order="no_fp desc",
                limit=1,
            )

            if existing:
                last_no_fp = existing[0].no_fp or ""
                # Extract the numeric part from the last used no_fp
                last_dot_idx = last_no_fp.rfind(".")
                if last_dot_idx >= 0:
                    try:
                        last_num = int(last_no_fp[last_dot_idx + 1 :])
                        next_num = last_num + 1
                    except ValueError:
                        next_num = num_start
                else:
                    import re

                    m = re.match(r"^(.*?)(\d+)$", last_no_fp)
                    if m:
                        next_num = int(m.group(2)) + 1
                    else:
                        next_num = num_start
            else:
                next_num = num_start

            if next_num > num_end:
                return error_response(
                    f"Range penomoran sudah habis! Maksimal: {prefix}{str(num_end).zfill(num_len)}"
                )

            new_no_fp = (
                f"{kode_transaksi}{kode_status}.{prefix}{str(next_num).zfill(num_len)}"
            )

            return success_response(
                "Nomor FP berhasil digenerate", {"no_fp": new_no_fp}
            )
        except Exception as e:
            _logger.error("Error auto_no_fp: %s", str(e))
            return error_response(str(e))
