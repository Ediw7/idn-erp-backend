## [0.1.2](https://github.com/Ediw7/idn-erp-backend/compare/v0.1.1...v0.1.2) (2026-07-12)


### Bug Fixes

* **history-harga:** fix kwargs search domain and null is_void bug ([1b5dded](https://github.com/Ediw7/idn-erp-backend/commit/1b5dded691da1867c6b51f36e2e023190b156fbd))



## [0.1.1](https://github.com/Ediw7/idn-erp-backend/compare/v0.1.0...v0.1.1) (2026-07-11)


### Bug Fixes

* merge format and changelog to prevent race condition ([37b6367](https://github.com/Ediw7/idn-erp-backend/commit/37b63673ae874687adac609f936a1cb731413fb8))



# [0.1.0](https://github.com/Ediw7/idn-erp-backend/compare/e94f90dd392f2775231da78552935da8cfb48679...v0.1.0) (2026-07-11)


### Bug Fixes

* akses user ke setup perusahaan ([89fae3e](https://github.com/Ediw7/idn-erp-backend/commit/89fae3ea8ba939220d76252a3f465ed4f0467737))
* **api_outstanding:** remove invalid proyek attribute from sales_order to fix 500 error ([0525cbf](https://github.com/Ediw7/idn-erp-backend/commit/0525cbff70b95b687326769ccc558213372e5ebf))
* **backend:** fix race conditions and add db constraints for SO and SJ ([872eabe](https://github.com/Ediw7/idn-erp-backend/commit/872eabec7ab739438f6e21ea2e14445962afe770))
* comment out deploy job missing secrets ([2bb4965](https://github.com/Ediw7/idn-erp-backend/commit/2bb4965e34202263064a02f2b5a17ddccd2d16d5))
* docker tag lowercase issue ([9400746](https://github.com/Ediw7/idn-erp-backend/commit/9400746a71649c48afcf3acbe612a186cde7c39c))
* error setup perusahaan ([b483c07](https://github.com/Ediw7/idn-erp-backend/commit/b483c07983e402fd4126c04963ba4783c69d9453))
* **finance:** hardened invoice-payment logic and resolved overpayment vulnerabilities ([edcd32a](https://github.com/Ediw7/idn-erp-backend/commit/edcd32abc45c06228d389a7b2165b97fee40933d))
* Implement server-side uniqueness constraint and auto-no generation for transactions ([d267e04](https://github.com/Ediw7/idn-erp-backend/commit/d267e044a86d9c0743bcec64df3a9657f306f50b))
* **invoice:** fix invoice deletion logic on 0 value & update surat jalan edit lock ([caef6f9](https://github.com/Ediw7/idn-erp-backend/commit/caef6f94e56f4f08adc3ade44010be9eae4ec1e7))
* **invoice:** resolve double invoicing & SJ sync issues ([7a2f46d](https://github.com/Ediw7/idn-erp-backend/commit/7a2f46db7eb50ad72c8493794d0345fee393eda9))
* memeperbaiki setup awal ([ee0a14f](https://github.com/Ediw7/idn-erp-backend/commit/ee0a14f1cbc01fd5927ab414f16584e3a258e177))
* **security:** enforce strict multi-tenant isolation and smart user restore workflow ([5029196](https://github.com/Ediw7/idn-erp-backend/commit/50291962ec06eb0d72f8558d2a2140093490b3cc))
* **setup:** implement robust tax exchange rate validation & refine UI placeholders ([d1f9d0e](https://github.com/Ediw7/idn-erp-backend/commit/d1f9d0e2ebc113833309c5ea9b90a98fcdc2e50d))


### Features

* add auto formatter, changelog, and codecov ([34eaa94](https://github.com/Ediw7/idn-erp-backend/commit/34eaa9481aabdfcfd3d44760683de6a0efebe3e7))
* Added invoicingbackend.saldo_awal_piutang model and CRUD API ([77a178a](https://github.com/Ediw7/idn-erp-backend/commit/77a178a20f8e9306d6312eb56f93ceff3d8f3443))
* **backend:** complete invoicing and AR modules ([ab9b9dd](https://github.com/Ediw7/idn-erp-backend/commit/ab9b9dd668680c87191af4c19b17c501778ba567))
* **company:** implement dynamic serial number generation ([03c0495](https://github.com/Ediw7/idn-erp-backend/commit/03c049502aa77818fbc60abc314170b98226b48d))
* enforce strict RBAC on frontend and fix Odoo read access rules ([3a0afc7](https://github.com/Ediw7/idn-erp-backend/commit/3a0afc7080d45d686dfbca707c1a622eb52a4e33))
* **erp:** Full-Stack Migration, Security Fixes, and Query Optimization ([120d015](https://github.com/Ediw7/idn-erp-backend/commit/120d0152100ea25878623475e962905354fa47b8))
* Finalisasi migrasi full-backend, implementasi API hapus (POST) di semua modul transaksi, dan optimasi auto-fill form Kwitansi.: ([7283d18](https://github.com/Ediw7/idn-erp-backend/commit/7283d184e91db855362fd8cd3c46e6c91d124d2c))
* **invoice:** activate PPh 22 calculation in frontend and backend ([f56163a](https://github.com/Ediw7/idn-erp-backend/commit/f56163a0ff05877894cfdb5c13fd36ca11d54529))
* **invoice:** map is_void from frontend and prevent duplicate surat jalan ([b01ac05](https://github.com/Ediw7/idn-erp-backend/commit/b01ac0587feffc9817255959209f753fc80b0e79))
* **invoice:** return more complete data for outstanding invoice list ([40fca0e](https://github.com/Ediw7/idn-erp-backend/commit/40fca0e8dd04bb6ef82c4d5128a388000800706a))
* **invoice:** support multiple surat jalan per invoice ([28bcc6e](https://github.com/Ediw7/idn-erp-backend/commit/28bcc6ecaa05f9f73c0c7fb7bdba55e5e9b7ab03))
* **invoicing:** overhaul saldo awal piutang UI and API architecture ([d7fad67](https://github.com/Ediw7/idn-erp-backend/commit/d7fad670ebd4b96c271d62330d1a08e972a9bc33))
* menambahkan fitur dari setup gudang sampe pembayran ([bf560db](https://github.com/Ediw7/idn-erp-backend/commit/bf560db62e75d78dcbbac4852009b24a5320a8b6))
* menambahkan fitur dari setup preferensi sampai perkiraan ([e94f90d](https://github.com/Ediw7/idn-erp-backend/commit/e94f90dd392f2775231da78552935da8cfb48679))
* **reporting:** rebuild report menu layout and implement PDF generation API ([0a126f8](https://github.com/Ediw7/idn-erp-backend/commit/0a126f821c2310c0aa69deead557ba46d346c2c3))
* revamp UI Faktur Pajak & restrukturisasi folder PPN ([15d5ff7](https://github.com/Ediw7/idn-erp-backend/commit/15d5ff75be9ae5336c5068830c8c174c5c691911))
* **saas:** migrate architecture to multi-tenant & implement closed B2B registration ([e2d9d56](https://github.com/Ediw7/idn-erp-backend/commit/e2d9d5698200ba724320c7cc03c43b95a9e5eaf2))
* **sales-order:** penambahan layout Surat Jalan dan integrasi Modal Laporan ([b183896](https://github.com/Ediw7/idn-erp-backend/commit/b1838967e5c9da14cf44c4b99fdeb34b692ec35c))
* **sales-order:** tambah sistem tab untuk Detail Barang, Surat Jalan, dan Outstanding ([f71facd](https://github.com/Ediw7/idn-erp-backend/commit/f71facdab80b472af87e361728507df341700fc8))
* **sales:** implement Cek History Harga Jual UI & auto-close SO logic ([891c18e](https://github.com/Ediw7/idn-erp-backend/commit/891c18e77b11a290c4f65c2b692c832f2492a980))
* **setup:** overhaul database initialization & setup perusahaan workflow ([fa8ac97](https://github.com/Ediw7/idn-erp-backend/commit/fa8ac973a082b65ec321b7523ce291de0a00d9ba))
* testing setup ([48717da](https://github.com/Ediw7/idn-erp-backend/commit/48717da522083b56ec00b693878b13a22de59623))



