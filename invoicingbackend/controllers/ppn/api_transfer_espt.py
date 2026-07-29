import csv
import io
from odoo import http
from odoo.http import request


class ApiTransferESpt(http.Controller):

    @http.route(
        "/api/transfer-espt/lampiran",
        type="http",
        auth="user",
        methods=["GET"],
        cors="http://localhost:5173",
    )
    def export_lampiran(self, **kw):
        tahun = kw.get("tahun", "")
        masa = kw.get("masa", "")
        jenis_lampiran = kw.get("jenis_lampiran", "1111A")

        output = io.StringIO()
        writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_ALL)

        # Search Faktur Pajak matching month and year
        # Assuming tgl_fp is used to filter month and year, or there is a specific field for it.
        # But wait, tgl_fp is a Date field. In Odoo, we can search date ranges.
        # Let's just fetch all and filter in Python for safety, or search properly.
        domain = []
        if tahun and masa:
            domain = [
                ("tgl_fp", ">=", f"{tahun}-{masa}-01"),
                ("tgl_fp", "<=", f"{tahun}-{masa}-31"),
            ]

        fakturs = request.env["invoicingbackend.transaksi_faktur_pajak"].search(domain)

        if jenis_lampiran == "1111A":
            writer.writerow(
                [
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

            for fp in fakturs:
                fg_pengganti = "1" if fp.fp_diganti else "0"
                npwp = fp.pembeli_id.npwp if fp.pembeli_id else ""
                nama = fp.pembeli_id.nama or fp.pembeli_id.nama_wp or ""
                alamat = fp.pembeli_id.alamat_wp or fp.pembeli_id.alamat or ""
                tgl = fp.tgl_fp.strftime("%Y-%m-%d") if fp.tgl_fp else ""

                writer.writerow(
                    [
                        fp.jenis_transaksi or "01",
                        fg_pengganti,
                        fp.no_fp or "",
                        masa.zfill(2),
                        tahun,
                        tgl,
                        npwp,
                        nama,
                        alamat,
                        int(fp.dpp_rp or 0),
                        int(fp.ppn_rp or 0),
                        0,  # PPNBM
                        fp.ket_tambahan or "",
                        "0",
                        int(fp.uang_muka or 0),
                        0,  # UANG MUKA PPN
                        0,  # UANG MUKA PPNBM
                        fp.no_invoice or "",
                    ]
                )
        else:
            # Fallback for 1111B or others (mocked for now since usually separate models or same logic but different format)
            writer.writerow(["Masa", "Tahun", "Nomor"])

        csv_data = output.getvalue()

        return request.make_response(
            csv_data,
            headers=[
                ("Content-Type", "text/csv"),
                (
                    "Content-Disposition",
                    f'attachment; filename="{jenis_lampiran}_{tahun}{masa.zfill(2)}.csv"',
                ),
            ],
        )

    @http.route(
        "/api/transfer-espt/wp",
        type="http",
        auth="user",
        methods=["GET"],
        cors="http://localhost:5173",
    )
    def export_wp(self, **kw):
        output = io.StringIO()
        writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_ALL)

        # Example headers for e-SPT Wajib Pajak (Lawan Transaksi)
        writer.writerow(
            [
                "NPWP",
                "NAMA",
                "JALAN",
                "BLOK",
                "NO",
                "RT",
                "RW",
                "KECAMATAN",
                "KELURAHAN",
                "KABUPATEN",
                "PROPINSI",
                "KODE_POS",
                "NOMOR_TELEPON",
            ]
        )

        pelanggans = request.env["invoicingbackend.pelanggan"].search([])
        for p in pelanggans:
            # Only export those with valid NPWP for e-SPT
            if not p.npwp or p.npwp == "00.000.000.0-000.000":
                pass  # Can still export, but usually we export all

            alamat = p.alamat_wp or p.alamat or ""

            writer.writerow(
                [
                    p.npwp or "00.000.000.0-000.000",
                    p.nama_wp or p.nama or "",
                    alamat,
                    "",  # BLOK
                    "",  # NO
                    "",  # RT
                    "",  # RW
                    "",  # KECAMATAN
                    "",  # KELURAHAN
                    "",  # KABUPATEN
                    "",  # PROPINSI
                    "",  # KODE_POS
                    p.telepon or "",
                ]
            )

        csv_data = output.getvalue()

        return request.make_response(
            csv_data,
            headers=[
                ("Content-Type", "text/csv"),
                ("Content-Disposition", 'attachment; filename="wp_lawantransaksi.csv"'),
            ],
        )

    @http.route(
        "/api/transfer-espt/pph22",
        type="http",
        auth="user",
        methods=["GET"],
        cors="http://localhost:5173",
    )
    def export_pph22(self, **kw):
        output = io.StringIO()
        writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_ALL)

        # Example dummy headers for e-SPT PPh 22
        writer.writerow(
            [
                "MASA_PAJAK",
                "TAHUN_PAJAK",
                "NPWP",
                "NAMA",
                "ALAMAT",
                "NO_BUKTI_POTONG",
                "TANGGAL_BUKTI_POTONG",
                "NILAI_OBJEK_PAJAK",
                "PPH_DIPOTONG",
            ]
        )

        csv_data = output.getvalue()

        return request.make_response(
            csv_data,
            headers=[
                ("Content-Type", "text/csv"),
                ("Content-Disposition", 'attachment; filename="pph22.csv"'),
            ],
        )
