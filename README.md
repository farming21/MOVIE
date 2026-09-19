# MOVIE

Website video + panel admin dalam satu repository.

## Aturan inti
- Kategori: Indonesia, Papua, Barat.
- Slug otomatis dari judul + Part.
- Part otomatis dihitung per kategori saat video baru dibuat.
- Edit video tidak mengubah slug/Part.
- Urutan website berdasarkan tanggal + jam publikasi, bukan waktu terakhir diedit.
- Cover: `covers/[slug].jpg`.
- OG cover: `covers/og/[slug].jpg`, 1200x630 px.
- Google Drive player tetap digunakan.
- `videos.json` adalah source of truth.
- GitHub Actions menjalankan generator dan deploy ke GitHub Pages.

## Admin
Buka `/admin/`. Panel memakai GitHub Personal Access Token yang dimasukkan sendiri oleh admin. Token hanya disimpan di sessionStorage browser. Token harus memiliki akses Contents: Read and write pada repository yang dikonfigurasi di Website Settings.

## Data publikasi
```json
{
  "tanggal": "2026-09-19",
  "jam": "21:30"
}
```

## Migrasi
Data lama dapat diimpor melalui `scripts/import_legacy.py` setelah URL legacy diisi secara manual jika diperlukan. Script hanya membaca `videos.json` lama; folder `covers/` lama tidak dibaca.

## GitHub Pages
Setelah upload ke branch `main`, buka Settings → Pages dan pilih GitHub Actions sebagai Source.
