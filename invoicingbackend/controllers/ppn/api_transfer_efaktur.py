import csv
import io
import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ApiTransferEFaktur(http.Controller):

    @http.route(
        "/api/export-efaktur",
        type="http",
        auth="user",
        methods=["GET"],
        cors="http://localhost:5173",
    )
    def export_efaktur(self, **kw):
        jenis_pajak = kw.get("jenis_pajak", "Pajak Keluaran")
        tahun = kw.get("tahun", "")
        bulan = kw.get("bulan", "")
        pembetulan = kw.get("pembetulan", "0")
        fp_awal = kw.get("fp_awal", "")
        fp_akhir = kw.get("fp_akhir", "")

        output = io.StringIO()
        writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_ALL)

        # Determine headers based on jenis_pajak
        if jenis_pajak == "Pajak Keluaran":
            writer.writerow(
                [
                    "FK",
                    "KD_JENIS_TRANSAKSI",
                    "FG_PENGGANTI",
                    "NOMOR_FAKTUR",
                    "MASA_PAJAK",
                    "TAHUN_PAJAK",
                    "TANGGAL_FAKTUR",
                    "NPWP",
                    "NAMA",
                    "ALAMAT_LENGKAP",
                    "JUMLAH_DPP",
                    "JUMLAH_PPN",
                    "JUMLAH_PPNBM",
                    "ID_KETERANGAN_TAMBAHAN",
                    "FG_UANG_MUKA",
                    "UANG_MUKA_DPP",
                    "UANG_MUKA_PPN",
                    "UANG_MUKA_PPNBM",
                    "REFERENSI",
                ]
            )
            # Search real Faktur Pajak
            domain = []
            if tahun and bulan:
                domain.extend([
                    ("tgl_fp", ">=", f"{tahun}-{bulan}-01"),
                    ("tgl_fp", "<=", f"{tahun}-{bulan}-31"),
                ])
            
            fakturs = request.env["invoicingbackend.transaksi_faktur_pajak"].search(domain)
            
            for fp in fakturs:
                # Basic string filtering for fp_awal and fp_akhir if provided
                if fp_awal and fp_awal > (fp.no_fp or ""):
                    continue
                if fp_akhir and fp_akhir < (fp.no_fp or ""):
                    continue

                fg_pengganti = "1" if fp.fp_diganti else "0"
                npwp = fp.pembeli_id.npwp if fp.pembeli_id else ""
                nama = fp.pembeli_id.nama_wp or fp.pembeli_id.nama or ""
                alamat = fp.pembeli_id.alamat_wp or fp.pembeli_id.alamat or ""
                tgl = fp.tgl_fp.strftime("%Y-%m-%d") if fp.tgl_fp else ""
                jenis = fp.jenis_transaksi.split(" ")[0] if fp.jenis_transaksi else "01"

                writer.writerow(
                    [
                        "FK",
                        jenis,
                        fg_pengganti,
                        fp.no_fp or "",
                        bulan.zfill(2),
                        tahun,
                        tgl,
                        npwp,
                        nama,
                        alamat,
                        int(fp.dpp_rp or 0),
                        int(fp.ppn_rp or 0),
                        0,  # PPNBM
                        fp.ket_tambahan or "",
                        "0", # FG UANG MUKA
                        int(fp.uang_muka or 0),
                        0, # UANG MUKA PPN
                        0, # UANG MUKA PPNBM
                        fp.no_invoice or "",
                    ]
                )
        elif jenis_pajak == "Pajak Masukan":
            writer.writerow(
                [
                    "FM",
                    "KD_JENIS_TRANSAKSI",
                    "FG_PENGGANTI",
                    "NOMOR_FAKTUR",
                    "MASA_PAJAK",
                    "TAHUN_PAJAK",
                    "TANGGAL_FAKTUR",
                    "NPWP",
                    "NAMA",
                    "ALAMAT_LENGKAP",
                    "JUMLAH_DPP",
                    "JUMLAH_PPN",
                    "JUMLAH_PPNBM",
                    "IS_CREDITABLE",
                ]
            )
            # No table for Masukan yet, keeping headers only
        else:
            # For Retur
            writer.writerow(
                [
                    "RETUR",
                    "NOMOR_RETUR",
                    "NOMOR_FAKTUR_YANG_DIRETUR",
                    "NPWP_LAWAN_TRANSAKSI",
                    "NAMA_LAWAN_TRANSAKSI",
                    "TANGGAL_RETUR",
                    "DPP",
                    "PPN",
                    "PPNBM",
                ]
            )
            # Search real Nota Retur
            domain = []
            if tahun and bulan:
                domain.extend([
                    ("tgl_nota", ">=", f"{tahun}-{bulan}-01"),
                    ("tgl_nota", "<=", f"{tahun}-{bulan}-31"),
                ])
            
            returs = request.env["invoicingbackend.nota_retur"].search(domain)

            for r in returs:
                npwp = r.pelanggan_id.npwp if r.pelanggan_id else ""
                nama = r.pelanggan_id.nama_wp or r.pelanggan_id.nama or ""
                tgl = r.tgl_nota.strftime("%Y-%m-%d") if r.tgl_nota else ""
                
                # Calculate total DPP and PPN from lines
                total_dpp = sum((line.harga_jual * line.kuantum) for line in r.line_ids)
                total_ppn = total_dpp * (r.tarif_ppn / 100.0) if r.tarif_ppn else 0

                writer.writerow(
                    [
                        "RETUR",
                        r.no_nota or "",
                        r.atas_no_fp or "",
                        npwp,
                        nama,
                        tgl,
                        int(total_dpp),
                        int(total_ppn),
                        0, # PPNBM
                    ]
                )

        csv_data = output.getvalue()

        formatted_jenis = jenis_pajak.replace(" ", "_")
        filename = f"{formatted_jenis}_{tahun}{bulan.zfill(2)}.csv"

        return request.make_response(
            csv_data,
            headers=[
                ("Content-Type", "text/csv"),
                ("Content-Disposition", f'attachment; filename="{filename}"'),
            ],
        )
