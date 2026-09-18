# farming21/movie

Website video + panel admin dalam **satu repository**.

## Fitur utama

- Kategori tetap: **Indonesia**, **Papua**, **Barat**.
- Slug otomatis dari judul.
- Part otomatis per kategori: `part1`, `part2`, `part3`, dan seterusnya.
- Saat video lama diedit, slug/Part tidak berubah.
- Urutan website berdasarkan **tanggal + jam publikasi**, bukan waktu terakhir diedit.
- Google Drive player.
- Cover lokal untuk video baru.
- Cover video lama tidak disalin atau dibaca; generator memakai cover publik dari repository lama sampai cover baru diganti.
- GitHub Actions menghasilkan halaman video dan deploy ke GitHub Pages.
- `admin/` menjadi pengganti panel RepoPilot-AI dalam repository yang sama.

## Admin

Buka:

`https://farming21.github.io/movie/admin/`

Panel menggunakan GitHub Personal Access Token yang kamu masukkan sendiri. Token hanya disimpan di `sessionStorage` browser.

Untuk repository `farming21/movie`, token harus memiliki izin **Contents: Read and write**.

## Data

`videos.json` adalah source of truth.

Field publikasi:

```json
{
  "tanggal": "2026-09-19",
  "jam": "21:30"
}
```

Video dengan tanggal sama diurutkan berdasarkan jam. Mengedit judul/deskripsi/cover tidak mengubah urutan selama tanggal dan jam publikasi tidak diubah.

## Migrasi dari farming21/indonesia

Saat pertama kali build, workflow menjalankan `scripts/import_legacy.py` jika `videos.json` masih `[]`. Script mengambil `videos.json` lama dari repository publik dan hanya menambahkan `jam: "00:00"` untuk data lama. **Folder `covers/` lama tidak dibaca.**

Cover lama tetap ditampilkan dari:

`https://farming21.github.io/indonesia/covers/...`

Ketika kamu upload cover baru melalui Admin, file disimpan ke `covers/` di repository `movie`.

## GitHub Pages

Workflow menggunakan GitHub Actions untuk generate `index.html` dan `videos/*.html`, lalu deploy ke GitHub Pages.

Setelah file di-upload ke `main`, buka Settings → Pages dan pilih **GitHub Actions** sebagai Source bila belum terpilih.
