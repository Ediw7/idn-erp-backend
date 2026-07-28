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
            # Example dummy row
            writer.writerow(
                [
                    "FK",
                    "01",
                    "0",
                    f"{fp_awal or '0000000000000'}",
                    bulan.zfill(2),
                    tahun,
                    f"{tahun}-{bulan.zfill(2)}-01",
                    "00.000.000.0-000.000",
                    "PT DUMMY KELUARAN",
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
            writer.writerow(
                [
                    "FM",
                    "01",
                    "0",
                    f"{fp_awal or '0000000000000'}",
                    bulan.zfill(2),
                    tahun,
                    f"{tahun}-{bulan.zfill(2)}-01",
                    "00.000.000.0-000.000",
                    "PT DUMMY MASUKAN",
                    "JAKARTA",
                    "1000000",
                    "110000",
                    "0",
                    "1",
                ]
            )
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
            writer.writerow(
                [
                    "RETUR",
                    "NR-001",
                    f"{fp_awal or '0000000000000'}",
                    "00.000.000.0-000.000",
                    "PT DUMMY RETUR",
                    f"{tahun}-{bulan.zfill(2)}-01",
                    "1000000",
                    "110000",
                    "0",
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
