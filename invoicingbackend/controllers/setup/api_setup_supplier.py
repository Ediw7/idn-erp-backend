from odoo import http
from odoo.http import request


class ApiSetupSupplier(http.Controller):

    @http.route(
        "/api/setup/supplier/get", type="json", auth="user", methods=["POST"], cors="*"
    )
    def get_supplier(self, **kw):
        try:
            records = request.env["invoicingbackend.supplier"].search(
                [], order="kode asc"
            )
            data = []
            for rec in records:
                data.append(
                    {
                        "id": rec.id,
                        "kode": rec.kode or "",
                        "nama": rec.nama or "",
                        "alamat": rec.alamat or "",
                        "telepon": rec.telepon or "",
                        "fax": rec.fax or "",
                        "email": rec.email or "",
                        "contact_person": rec.contact_person or "",
                        "no_hp": rec.no_hp or "",
                        "nama_wp": rec.nama_wp or "",
                        "alamat_wp": rec.alamat_wp or "",
                        "npwp": rec.npwp or "",
                        "tgl_pengukuhan": (
                            str(rec.tgl_pengukuhan) if rec.tgl_pengukuhan else ""
                        ),
                        "no_seri_fp_masukan": rec.no_seri_fp_masukan or "",
                        "is_pkp": rec.is_pkp,
                        "jenis_transaksi": rec.jenis_transaksi or "01",
                        "pembayaran_id": (
                            rec.pembayaran_id.id if rec.pembayaran_id else None
                        ),
                        "pembayaran_nama": (
                            rec.pembayaran_id.nama if rec.pembayaran_id else ""
                        ),
                        "keterangan": rec.keterangan or "",
                    }
                )
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @http.route(
        "/api/setup/supplier/save", type="json", auth="user", methods=["POST"], cors="*"
    )
    def save_supplier(self, **kw):
        try:
            params = kw
            record_id = params.get("id")

            vals = {
                "kode": params.get("kode"),
                "nama": params.get("nama"),
                "alamat": params.get("alamat"),
                "telepon": params.get("telepon"),
                "fax": params.get("fax"),
                "email": params.get("email"),
                "contact_person": params.get("contact_person"),
                "no_hp": params.get("no_hp"),
                "nama_wp": params.get("nama_wp"),
                "alamat_wp": params.get("alamat_wp"),
                "npwp": params.get("npwp"),
                "tgl_pengukuhan": params.get("tgl_pengukuhan") or False,
                "no_seri_fp_masukan": params.get("no_seri_fp_masukan"),
                "is_pkp": bool(params.get("is_pkp", False)),
                "jenis_transaksi": params.get("jenis_transaksi") or "01",
                "pembayaran_id": params.get("pembayaran_id") or False,
                "keterangan": params.get("keterangan"),
            }

            if record_id:
                record = request.env["invoicingbackend.supplier"].browse(record_id)
                if record.exists():
                    record.write(vals)
                else:
                    return {"status": "error", "message": "Data tidak ditemukan"}
            else:
                vals["company_id"] = request.env.user.company_id.id
                record = request.env["invoicingbackend.supplier"].create(vals)

            return {
                "status": "success",
                "message": "Supplier berhasil disimpan",
                "id": record.id,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @http.route(
        "/api/setup/supplier/delete",
        type="json",
        auth="user",
        methods=["POST"],
        cors="*",
    )
    def delete_supplier(self, **kw):
        try:
            params = kw
            record_id = params.get("id")

            if record_id:
                record = request.env["invoicingbackend.supplier"].browse(record_id)
                if record.exists():
                    record.unlink()
                    return {"status": "success", "message": "Supplier berhasil dihapus"}
                else:
                    return {"status": "error", "message": "Data tidak ditemukan"}
            return {"status": "error", "message": "ID tidak valid"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
