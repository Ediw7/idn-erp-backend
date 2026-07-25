from odoo import http
from odoo.http import request
import json
from .api_response import ApiResponse
from datetime import datetime

class ApiNotaKredit(http.Controller):

    @http.route("/api/nota-kredit", type="http", auth="user", methods=["GET", "OPTIONS"], csrf=False, cors="http://localhost:5173")
    def get_all_nota_kredit(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return ApiResponse.success()
        try:
            domain = []
            
            # Filters
            periode = kwargs.get("periode")
            if periode:
                domain.append(("periode", "=", periode))
            
            # Search
            search = kwargs.get("search")
            if search:
                domain.append("|")
                domain.append(("no_nota_kredit", "ilike", search))
                domain.append(("pelanggan_id.nama", "ilike", search))
                
            pelanggan_id = kwargs.get("pelanggan_id")
            if pelanggan_id:
                domain.append(("pelanggan_id", "=", int(pelanggan_id)))

            page = kwargs.get("page")
            limit = int(kwargs.get("limit", 2000))

            nota_kredit_obj = request.env["invoicingbackend.nota_kredit"]
            total_records = nota_kredit_obj.search_count(domain)

            if page:
                page = int(page)
                offset = (page - 1) * limit
                records = nota_kredit_obj.search(domain, limit=limit, offset=offset, order="create_date desc")
            else:
                page = 1
                records = nota_kredit_obj.search(domain, limit=limit, order="create_date desc")

            data = []
            for r in records:
                data.append({
                    "id": r.id,
                    "no_nota_kredit": r.no_nota_kredit,
                    "tgl_nota_kredit": r.tgl_nota_kredit.strftime("%Y-%m-%d") if r.tgl_nota_kredit else None,
                    "periode": r.periode,
                    "pelanggan_id": r.pelanggan_id.id if r.pelanggan_id else None,
                    "pelanggan_nama": r.pelanggan_id.nama if r.pelanggan_id else None,
                    "alamat": r.alamat,
                    "invoice_id": r.invoice_id.id if r.invoice_id else None,
                    "no_invoice": r.invoice_id.no_invoice if r.invoice_id else None,
                    "no_referensi": r.no_referensi,
                    "mata_uang_id": r.mata_uang_id.id if r.mata_uang_id else None,
                    "mata_uang_nama": r.mata_uang_id.nama if r.mata_uang_id else None,
                    "nilai_nota_kredit": r.nilai_nota_kredit,
                    "tanda_tangan": r.tanda_tangan,
                    "jabatan": r.jabatan,
                    "create_date": r.create_date.strftime("%Y-%m-%d %H:%M:%S") if r.create_date else None,
                    "create_uid": r.create_uid.name if r.create_uid else None,
                })
            
            pagination = {
                "total": total_records,
                "page": page,
                "limit": limit,
                "last_page": (total_records + limit - 1) // limit if limit else 1
            }

            return ApiResponse.success(message="Data Nota Kredit berhasil diambil", data=data, pagination=pagination)
        except Exception as e:
            return ApiResponse.error(str(e))

    @http.route("/api/nota-kredit/<int:nk_id>", type="http", auth="user", methods=["GET", "OPTIONS"], csrf=False, cors="http://localhost:5173")
    def get_nota_kredit_by_id(self, nk_id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return ApiResponse.success()
        try:
            record = request.env["invoicingbackend.nota_kredit"].browse(nk_id)
            if not record.exists():
                return ApiResponse.error("Nota Kredit tidak ditemukan", 404)

            lines = []
            for line in record.line_ids:
                lines.append({
                    "id": line.id,
                    "keterangan": line.keterangan,
                    "jumlah": line.jumlah,
                    "no_perkiraan": line.no_perkiraan,
                })

            data = {
                "id": record.id,
                "no_nota_kredit": record.no_nota_kredit,
                "tgl_nota_kredit": record.tgl_nota_kredit.strftime("%Y-%m-%d") if record.tgl_nota_kredit else None,
                "periode": record.periode,
                "pelanggan_id": record.pelanggan_id.id if record.pelanggan_id else None,
                "pelanggan_nama": record.pelanggan_id.nama if record.pelanggan_id else None,
                "alamat": record.alamat,
                "invoice_id": record.invoice_id.id if record.invoice_id else None,
                "no_invoice": record.invoice_id.no_invoice if record.invoice_id else None,
                "no_referensi": record.no_referensi,
                "mata_uang_id": record.mata_uang_id.id if record.mata_uang_id else None,
                "tanda_tangan": record.tanda_tangan,
                "jabatan": record.jabatan,
                "nilai_nota_kredit": record.nilai_nota_kredit,
                "lines": lines,
            }
            return ApiResponse.success(message="Detail Nota Kredit berhasil diambil", data=data)
        except Exception as e:
            return ApiResponse.error(str(e))

    @http.route("/api/nota-kredit", type="http", auth="user", methods=["POST", "OPTIONS"], csrf=False, cors="http://localhost:5173")
    def create_nota_kredit(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return ApiResponse.success()
        try:
            payload = json.loads(request.httprequest.data)
            
            lines_data = payload.get("lines", [])
            lines_vals = []
            for line in lines_data:
                lines_vals.append((0, 0, {
                    "keterangan": line.get("keterangan"),
                    "jumlah": float(line.get("jumlah", 0)),
                    "no_perkiraan": line.get("no_perkiraan"),
                }))

            vals = {
                "no_nota_kredit": payload.get("no_nota_kredit"),
                "tgl_nota_kredit": payload.get("tgl_nota_kredit"),
                "periode": payload.get("periode"),
                "pelanggan_id": int(payload.get("pelanggan_id")) if payload.get("pelanggan_id") else False,
                "invoice_id": int(payload.get("invoice_id")) if payload.get("invoice_id") else False,
                "no_referensi": payload.get("no_referensi"),
                "mata_uang_id": int(payload.get("mata_uang_id")) if payload.get("mata_uang_id") else False,
                "tanda_tangan": payload.get("tanda_tangan"),
                "jabatan": payload.get("jabatan"),
                "line_ids": lines_vals,
            }

            new_record = request.env["invoicingbackend.nota_kredit"].create(vals)
            return ApiResponse.success(message="Nota Kredit berhasil dibuat", data={"id": new_record.id, "no_nota_kredit": new_record.no_nota_kredit})
        except Exception as e:
            return ApiResponse.error(str(e))

    @http.route("/api/nota-kredit/<int:nk_id>", type="http", auth="user", methods=["PUT", "OPTIONS"], csrf=False, cors="http://localhost:5173")
    def update_nota_kredit(self, nk_id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return ApiResponse.success()
        try:
            record = request.env["invoicingbackend.nota_kredit"].browse(nk_id)
            if not record.exists():
                return ApiResponse.error("Nota Kredit tidak ditemukan", 404)

            payload = json.loads(request.httprequest.data)
            
            lines_data = payload.get("lines")
            lines_vals = []
            if lines_data is not None:
                # Remove old lines not in new payload
                new_line_ids = [l.get("id") for l in lines_data if l.get("id")]
                for old_line in record.line_ids:
                    if old_line.id not in new_line_ids:
                        lines_vals.append((2, old_line.id, False))
                
                # Add/Update lines
                for line in lines_data:
                    line_val = {
                        "keterangan": line.get("keterangan"),
                        "jumlah": float(line.get("jumlah", 0)),
                        "no_perkiraan": line.get("no_perkiraan"),
                    }
                    if line.get("id"):
                        lines_vals.append((1, line.get("id"), line_val))
                    else:
                        lines_vals.append((0, 0, line_val))

            vals = {}
            if "no_nota_kredit" in payload:
                vals["no_nota_kredit"] = payload["no_nota_kredit"]
            if "tgl_nota_kredit" in payload:
                vals["tgl_nota_kredit"] = payload["tgl_nota_kredit"]
            if "periode" in payload:
                vals["periode"] = payload["periode"]
            if "pelanggan_id" in payload:
                vals["pelanggan_id"] = int(payload["pelanggan_id"]) if payload["pelanggan_id"] else False
            if "invoice_id" in payload:
                vals["invoice_id"] = int(payload["invoice_id"]) if payload["invoice_id"] else False
            if "no_referensi" in payload:
                vals["no_referensi"] = payload["no_referensi"]
            if "mata_uang_id" in payload:
                vals["mata_uang_id"] = int(payload["mata_uang_id"]) if payload["mata_uang_id"] else False
            if "tanda_tangan" in payload:
                vals["tanda_tangan"] = payload["tanda_tangan"]
            if "jabatan" in payload:
                vals["jabatan"] = payload["jabatan"]
            if lines_vals:
                vals["line_ids"] = lines_vals

            record.write(vals)
            return ApiResponse.success(message="Nota Kredit berhasil diupdate", data={"id": record.id})
        except Exception as e:
            return ApiResponse.error(str(e))

    @http.route("/api/nota-kredit/<int:nk_id>", type="http", auth="user", methods=["DELETE", "OPTIONS"], csrf=False, cors="http://localhost:5173")
    def delete_nota_kredit(self, nk_id, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return ApiResponse.success()
        try:
            record = request.env["invoicingbackend.nota_kredit"].browse(nk_id)
            if not record.exists():
                return ApiResponse.error("Nota Kredit tidak ditemukan", 404)
            record.unlink()
            return ApiResponse.success(message="Nota Kredit berhasil dihapus")
        except Exception as e:
            return ApiResponse.error(str(e))

    @http.route("/api/nota-kredit/auto-no", type="http", auth="user", methods=["GET", "OPTIONS"], csrf=False, cors="http://localhost:5173")
    def get_nota_kredit_auto_no(self, **kwargs):
        if request.httprequest.method == "OPTIONS":
            return ApiResponse.success()
        try:
            # Check setup for auto no
            now = datetime.now()
            y = str(now.year)
            m = str(now.month).zfill(2)
            periode = f"{y}{m}"

            setup = request.env["invoicingbackend.format_bukti"].search([("periode", "=", periode)], limit=1)
            
            prefix = "NK/"
            suffix = f"/{m}/{y}"
            digit = 3

            if setup:
                if setup.nota_kredit_prefiks: prefix = setup.nota_kredit_prefiks
                if setup.nota_kredit_sufiks: suffix = setup.nota_kredit_sufiks
                if setup.nota_kredit_digit: digit = int(setup.nota_kredit_digit)

            # Find latest
            domain = [("no_nota_kredit", "ilike", prefix + "%" + suffix)]
            last_record = request.env["invoicingbackend.nota_kredit"].search(domain, order="no_nota_kredit desc", limit=1)

            next_num = 1
            if last_record and last_record.no_nota_kredit:
                last_no = last_record.no_nota_kredit
                try:
                    # NK/001/03/2026 -> extract 001
                    core = last_no.replace(prefix, "").replace(suffix, "")
                    next_num = int(core) + 1
                except:
                    pass
            
            auto_no = f"{prefix}{str(next_num).zfill(digit)}{suffix}"
            return ApiResponse.success(message="Auto No berhasil digenerate", data={"auto_no": auto_no})
        except Exception as e:
            return ApiResponse.error(str(e))
