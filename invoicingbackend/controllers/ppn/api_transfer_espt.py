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

        # Example dummy headers for e-SPT Lampiran
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

            # TODO: Fetch from actual FakturPajak if needed
            writer.writerow(
                [
                    "01",
                    "0",
                    "010.000-26.00000001",
                    masa.zfill(2),
                    tahun,
                    "2026-07-25",
                    "00.000.000.0-000.000",
                    "PT CONTOH",
                    "JAKARTA",
                    "1000000",
                    "110000",
                    "0",
                    "",
                    "0",
                    "0",
                    "0",
                    "0",
                    "",
                ]
            )
        else:
            writer.writerow(["Kolom1", "Kolom2", "Kolom3"])

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

        # Example dummy headers for e-SPT Wajib Pajak (Lawan Transaksi)
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

        # TODO: Fetch from actual Pelanggan if needed
        writer.writerow(
            [
                "00.000.000.0-000.000",
                "PT CONTOH",
                "JL SUDIRMAN",
                "",
                "1",
                "",
                "",
                "",
                "",
                "JAKARTA",
                "DKI JAKARTA",
                "",
                "",
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
