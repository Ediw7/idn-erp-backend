from odoo import http

# pyrefly: ignore [missing-import]
from odoo.http import request
import json
from datetime import datetime


class ApiFakturPajak(http.Controller):

    @http.route(
        "/api/faktur_pajak/get",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def get_faktur_pajak(self, **kw):
        try:
            domain = []

            # Additional filters can be passed in kwargs if needed

            records = (
                request.env["invoicingbackend.transaksi_faktur_pajak"]
                .sudo()
                .search(domain, order="tgl_fp desc, id desc", limit=2000)
            )

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

            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @http.route(
        "/api/faktur_pajak/save",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def save_faktur_pajak(self, **kw):
        try:
            payload = request.jsonrequest

            # Format dates properly
            tgl_fp = payload.get("tgl_fp")
            tgl_fp_diganti = payload.get("tgl_fp_diganti")

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

            if tgl_fp:
                vals["tgl_fp"] = tgl_fp
            if tgl_fp_diganti:
                vals["tgl_fp_diganti"] = tgl_fp_diganti

            fp_id = payload.get("id")
            if fp_id:
                rec = (
                    request.env["invoicingbackend.transaksi_faktur_pajak"]
                    .sudo()
                    .browse(fp_id)
                )
                if rec.exists():
                    rec.write(vals)
                else:
                    rec = (
                        request.env["invoicingbackend.transaksi_faktur_pajak"]
                        .sudo()
                        .create(vals)
                    )
            else:
                rec = (
                    request.env["invoicingbackend.transaksi_faktur_pajak"]
                    .sudo()
                    .create(vals)
                )

            # Process lines
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
                    request.env[
                        "invoicingbackend.transaksi_faktur_pajak_line"
                    ].sudo().browse(line_id).write(line_vals)
                    new_line_ids.append(line_id)
                else:
                    new_line = (
                        request.env["invoicingbackend.transaksi_faktur_pajak_line"]
                        .sudo()
                        .create(line_vals)
                    )
                    new_line_ids.append(new_line.id)

            # Remove deleted lines
            lines_to_delete = set(existing_line_ids) - set(new_line_ids)
            if lines_to_delete:
                request.env[
                    "invoicingbackend.transaksi_faktur_pajak_line"
                ].sudo().browse(list(lines_to_delete)).unlink()

            return {"status": "success", "id": rec.id}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @http.route(
        "/api/faktur_pajak/delete",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def delete_faktur_pajak(self, **kw):
        try:
            payload = request.jsonrequest
            fp_id = payload.get("id")
            if not fp_id:
                return {"status": "error", "message": "ID is required"}

            rec = (
                request.env["invoicingbackend.transaksi_faktur_pajak"]
                .sudo()
                .browse(fp_id)
            )
            if rec.exists():
                rec.unlink()

            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
