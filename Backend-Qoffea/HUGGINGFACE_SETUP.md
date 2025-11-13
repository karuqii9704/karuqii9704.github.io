# Setup Model dari Hugging Face

## Perubahan Utama

Backend Qoffea sekarang menggunakan model yang dioptimalkan dari Hugging Face repository alih-alih dari folder lokal.

### Repository Model

- **Repository**: [rakaval/Qoffea_2](https://huggingface.co/spaces/rakaval/Qoffea_2)
- **Type**: Hugging Face Space
- **Model File**: `best.pt`

## Cara Kerja

1. **Download Otomatis**: Saat aplikasi pertama kali dijalankan, model akan otomatis diunduh dari Hugging Face
2. **Caching**: Model yang diunduh akan disimpan di folder `model_cache/` untuk menghindari download berulang
3. **Load Model**: Setelah download, model akan dimuat seperti biasa menggunakan Ultralytics YOLO

## Instalasi Dependencies

```powershell
pip install -r requirements.txt
```

Dependency baru yang ditambahkan:

- `huggingface_hub>=0.20.0` - untuk mengunduh model dari Hugging Face

## Konfigurasi

Buat file `.env` berdasarkan `.env.example`:

```env
# Hugging Face Model Configuration
HF_MODEL_REPO=rakaval/Qoffea_2
HF_MODEL_FILE=best.pt
MODEL_CACHE_DIR=model_cache
CONFIDENCE_THRESHOLD=0.5
```

### Penjelasan Konfigurasi:

- `HF_MODEL_REPO`: ID repository Hugging Face (format: `username/repo-name`)
- `HF_MODEL_FILE`: Nama file model di dalam repository (biasanya `best.pt`)
- `MODEL_CACHE_DIR`: Direktori untuk menyimpan cache model yang diunduh
- `CONFIDENCE_THRESHOLD`: Threshold confidence untuk deteksi (0.0 - 1.0)

## Menjalankan Aplikasi

```powershell
python app.py
```

Output yang diharapkan:

```
🚀 Initializing Qoffea Backend...
📥 Loading model from Hugging Face: rakaval/Qoffea_2
🔍 Downloading model from Hugging Face...
   Repository: rakaval/Qoffea_2
   File: best.pt
✅ Model downloaded to: [cache_path]
📦 Loading model...
✅ Model loaded successfully!
📊 Classes detected: {0: 'class1', 1: 'class2', ...}
```

## Keuntungan Menggunakan Hugging Face

1. **Versi Control**: Model di-host secara terpusat dengan version control
2. **Optimasi**: Model yang telah dioptimalkan untuk performa lebih baik
3. **Kolaborasi**: Lebih mudah untuk berbagi dan berkolaborasi
4. **Update Mudah**: Tinggal update model di repository, tidak perlu deploy ulang
5. **Space Efisien**: Tidak perlu menyimpan model besar di repository Git

## Troubleshooting

### Error: "Failed to load model from Hugging Face"

**Solusi**:

1. Pastikan koneksi internet stabil
2. Verifikasi nama repository benar: `rakaval/Qoffea_2`
3. Pastikan file `best.pt` ada di repository
4. Cek permission/access ke Hugging Face Space

### Model Download Lambat

**Solusi**:

- Download hanya terjadi sekali, model akan di-cache
- Jika ingin force re-download, hapus folder `model_cache/`

### Error: "ModuleNotFoundError: No module named 'huggingface_hub'"

**Solusi**:

```powershell
pip install huggingface_hub
```

## Struktur Folder

```
Backend-Qoffea/
├── app.py                 # Main application (updated)
├── config.py              # Configuration (updated)
├── requirements.txt       # Dependencies (updated)
├── modules/
│   └── model_loader.py   # Model loader (updated)
├── model_cache/          # Cache untuk model yang diunduh (auto-created)
├── uploads/              # Uploaded images
└── reports/              # Generated reports
```

## Catatan Penting

- Folder `model_cache/` akan dibuat otomatis saat aplikasi pertama kali dijalankan
- Model hanya perlu diunduh sekali, setelah itu akan menggunakan cache
- Jika model di Hugging Face diupdate, hapus cache untuk re-download
- Ukuran model biasanya cukup besar (beberapa MB hingga ratusan MB)

## Migrasi dari Model Lokal

Jika sebelumnya menggunakan model lokal di folder `models/`:

1. ✅ Update dependencies: `pip install -r requirements.txt`
2. ✅ Update konfigurasi di `.env`
3. ✅ Jalankan aplikasi - model akan otomatis diunduh
4. ⚠️ Optional: Folder `models/` lokal bisa dihapus atau di-backup

Model lokal tidak lagi digunakan setelah migrasi ini.
