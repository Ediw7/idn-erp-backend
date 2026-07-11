from odoo import http
from odoo.http import request


class ApiSetupPembayaran(http.Controller):

    @http.route(
        "/api/setup/pembayaran/get",
        type="json",
        auth="user",
        methods=["POST"],
        cors="*",
    )
    def get_pembayaran(self, **kw):
        try:
            records = request.env["invoicingbackend.pembayaran"].search(
                [], order="kode asc"
            )
            data = []
            for rec in records:
                data.append(
                    {
                        "id": rec.id,
                        "kode": rec.kode,
                        "nama": rec.nama,
                        "hari_jatuh_tempo": rec.hari_jatuh_tempo,
                    }
                )
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @http.route(
        "/api/setup/pembayaran/save",
        type="json",
        auth="user",
        methods=["POST"],
        cors="*",
    )
    def save_pembayaran(self, **kw):
        try:
            params = kw
            record_id = params.get("id")

            vals = {
                "kode": params.get("kode"),
                "nama": params.get("nama"),
                "hari_jatuh_tempo": int(params.get("hari_jatuh_tempo", 0)),
            }

            if record_id:
                record = request.env["invoicingbackend.pembayaran"].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {"status": "error", "message": "Data tidak ditemukan"}
            else:
                vals["company_id"] = request.env.user.company_id.id
                record = request.env["invoicingbackend.pembayaran"].create(vals)

            return {
                "status": "success",
                "message": "Cara Pembayaran berhasil disimpan",
                "id": record.id,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @http.route(
        "/api/setup/pembayaran/delete",
        type="json",
        auth="user",
        methods=["POST"],
        cors="*",
    )
    def delete_pembayaran(self, **kw):
        try:
            params = kw
            record_id = params.get("id")

            if record_id:
                record = request.env["invoicingbackend.pembayaran"].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {
                        "status": "success",
                        "message": "Cara Pembayaran berhasil dihapus",
                    }
                else:
                    return {"status": "error", "message": "Data tidak ditemukan"}
            return {"status": "error", "message": "ID tidak valid"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
