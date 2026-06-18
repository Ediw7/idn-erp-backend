from odoo import models, fields, api

class SetupPreferensi(models.Model):
    _name = 'invoicingbackend.preferensi'
    _description = 'Setup Preferensi Invoicing'
    _inherit = 'invoicingbackend.base_tenant'

    # Sistem & Database
    folder_database = fields.Char(string="Folder Database", default="D:\\")
    file_database = fields.Char(string="File Database", default="invcdat2020.MDB")
    folder_backup_data = fields.Char(string="Folder Backup Data", default="C:\\krishand\\invc\\601")
    folder_csv_faktur = fields.Char(string="Folder File CSV e-Faktur", default="C:\\krishand\\invc\\601")
    nama_file_logo = fields.Char(string="Nama File Logo", default="C:\\krishand\\invc\\601\\logo.jpg")
    lebar_logo = fields.Float(string="Lebar Gambar Logo (inch)", default=0.90)
    tinggi_logo = fields.Float(string="Tinggi Gambar Logo (inch)", default=0.75)
    dokumen_pemotongan_inventory = fields.Selection([
        ('Surat Jalan', 'Surat Jalan'),
        ('Invoice', 'Invoice')
    ], string="Dokumen Pemotongan Inventory", default='Surat Jalan')
    validasi_qty_minus_sj = fields.Boolean(string="Validasi Qty Stok Minus di SJ", default=True)
    validasi_qty_minus_so = fields.Boolean(string="Validasi Qty Stok Minus di SO", default=True)

    # Pajak & Desimal
    tarif_ppn = fields.Float(string="Tarif PPN (%)", default=10.00)
    tarif_pph22 = fields.Float(string="Tarif PPh 22 (%)", default=0.00)
    kode_cabang_fp = fields.Char(string="Kode Cabang FP", default="000")
    selisih_hari_invoice_faktur = fields.Integer(string="Selisih Hari Tgl Invoice dgn Faktur Pajak", default=0)
    notif_sisa_faktur_kurang_dari = fields.Integer(string="Notifikasi Sisa Faktur Kurang Dari", default=5)
    desimal_kuantum = fields.Integer(string="Desimal Kuantum", default=2)
    desimal_harga_satuan = fields.Integer(string="Desimal Harga Satuan", default=2)
    desimal_jumlah = fields.Integer(string="Desimal Jumlah", default=2)

    # Akuntansi & Cetakan
    umur_piutang_1_sd = fields.Integer(default=30)
    umur_piutang_2_mulai = fields.Integer(default=31)
    umur_piutang_2_sd = fields.Integer(default=60)
    umur_piutang_3_mulai = fields.Integer(default=61)
    umur_piutang_3_sd = fields.Integer(default=90)
    umur_piutang_4_mulai = fields.Integer(default=91)
    umur_piutang_4_sd = fields.Integer(default=120)
    umur_piutang_5_mulai = fields.Integer(default=121)

    perk_piutang = fields.Char(string="Perk. Piutang", default="1104")
    perk_penjualan = fields.Char(string="Perk. Penjualan", default="4101")
    perk_uang_muka_penj = fields.Char(string="Perk. Uang Muka Penj", default="2102")
    perk_disc_penjualan = fields.Char(string="Perk. Disc Penjualan", default="4103")
    perk_ppn = fields.Char(string="Perk. PPN", default="2109005")
    perk_pph22 = fields.Char(string="Perk. PPh 22", default="2109004")

    ket_lembar_3_fp = fields.Char(string="Ket. Lembar ke-3 FP", default="Lembar Ke-3 : Untuk Arsip")
    ket_lembar_4_fp = fields.Char(string="Ket. Lembar ke-4 FP", default="Lembar Ke-4 : Untuk Arsip")

    footer_invoice_vat = fields.Text(string="Keterangan Footer Invoice VAT")
    footer_invoice_non_vat = fields.Text(string="Keterangan Footer Invoice Non-VAT")
    footer_kwitansi_vat = fields.Text(string="Keterangan Footer Kwitansi VAT")
    footer_kwitansi_non_vat = fields.Text(string="Keterangan Footer Kwitansi Non-VAT")

    @api.model
    def get_preferences(self):
        pref = self.search([], limit=1)
        if not pref:
            pref = self.create({})
        return pref.read()[0]
