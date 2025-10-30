# QOFFEA - AI-Powered Coffee Grading System

![QOFFEA Logo](Frontend-Qoffea/Assets/Logo%20Qoffe%20Baru.png)

Sistem penilaian kualitas biji kopi menggunakan AI (YOLO) untuk mendeteksi dan mengklasifikasikan biji kopi menjadi kategori baik (good) dan cacat (defect).

## 📋 Prerequisites

Sebelum menjalankan aplikasi, pastikan Anda telah menginstall:

- **Python 3.8 atau lebih tinggi** (disarankan Python 3.9-3.11)
- **pip** (Python package manager)
- **Git** (opsional, untuk clone repository)

## 🚀 Cara Menjalankan Aplikasi

### 1️⃣ Clone atau Download Repository

```bash
# Jika menggunakan Git
git clone https://github.com/EdselSpth/Qoffea.git
cd Qoffea

# Atau download ZIP dan extract, lalu buka folder di terminal/command prompt
```

### 2️⃣ Buat Virtual Environment

**Untuk Windows (PowerShell/CMD):**

```powershell
# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
.venv\Scripts\activate

# Jika error "cannot be loaded because running scripts is disabled", jalankan:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Untuk Linux/Mac:**

```bash
# Buat virtual environment
python3 -m venv .venv

# Aktifkan virtual environment
source .venv/bin/activate
```

Setelah aktivasi berhasil, Anda akan melihat `(.venv)` di awal baris terminal.

### 3️⃣ Install Dependencies

Pastikan virtual environment sudah aktif, lalu install semua dependencies:

```bash
# Masuk ke folder Backend-Qoffea
cd Backend-Qoffea

# Install requirements
pip install -r requirements.txt
```

**Catatan:** Proses instalasi membutuhkan waktu beberapa menit karena akan mendownload PyTorch dan library lainnya.

### 4️⃣ Jalankan Backend Server

Setelah instalasi selesai, jalankan aplikasi:

**Cara 1 (Recommended):**

```bash
# Pastikan masih di folder Backend-Qoffea dan virtual environment aktif
python app.py
```

**Cara 2 (Dengan path lengkap):**

```powershell
# Windows - dari root folder Qoffea
cd Backend-Qoffea
..\\.venv\Scripts\python.exe app.py
```

```bash
# Linux/Mac - dari root folder Qoffea
cd Backend-Qoffea
../.venv/bin/python app.py
```

Jika berhasil, Anda akan melihat output seperti ini:

```
🔧 Using device: cpu
🚀 Initializing Qoffea Backend...
📦 Loading model from: E:\...\Backend-Qoffea\models\best.pt
✅ Model loaded successfully!
📊 Classes detected: {0: 'coffee-grade-break', 1: 'coffee-grade-good'}
✅ Model loaded successfully!
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.xx:5000
```

### 5️⃣ Akses Aplikasi

Setelah server berjalan, buka browser dan akses salah satu URL berikut:

| Halaman             | URL                           | Deskripsi                    |
| ------------------- | ----------------------------- | ---------------------------- |
| **Homepage**        | http://127.0.0.1:5000         | Halaman utama (Tentang Kami) |
| **Halaman Aksi** ⭐ | http://127.0.0.1:5000/aksi    | Upload & analisis biji kopi  |
| **Panduan Kerja**   | http://127.0.0.1:5000/panduan | Panduan penggunaan aplikasi  |

**Recommended:** Gunakan halaman **Aksi** untuk mulai menganalisis biji kopi!

## 📸 Cara Menggunakan Aplikasi

1. **Buka halaman Aksi:** http://127.0.0.1:5000/aksi
2. **Ambil/Upload Foto:**
   - Klik **"Buka Kamera"** untuk capture foto langsung dari kamera
   - Atau klik **"Pilih dari Galeri"** untuk upload foto dari perangkat
3. **Tunggu Analisis:** AI akan menganalisis gambar (≈1-2 detik)
4. **Lihat Hasil:**
   - Grade kualitas (A/B/C)
   - Persentase biji baik vs cacat
   - Jumlah total biji terdeteksi
   - Gambar dengan kotak deteksi
5. **Download PDF:** Klik tombol "Download Laporan PDF" untuk menyimpan hasil

## 📁 Struktur Project

```
Qoffea/
├── Backend-Qoffea/           # Backend Flask API
│   ├── models/               # Model AI (best.pt)
│   ├── modules/              # Core modules
│   │   ├── __init__.py
│   │   ├── model_loader.py   # YOLO model loader
│   │   ├── analyzer.py       # Analisis logika
│   │   ├── image_processor.py
│   │   └── pdf_generator.py  # Generate PDF report
│   ├── routes/               # API endpoints
│   │   ├── upload.py         # Upload & analyze
│   │   └── report.py         # PDF download
│   ├── utils/                # Helper utilities
│   ├── uploads/              # Temporary uploaded images
│   ├── reports/              # Generated PDF reports
│   ├── app.py               # ⭐ Main application
│   ├── config.py            # Configuration
│   └── requirements.txt     # Python dependencies
│
├── Frontend-Qoffea/         # Frontend files
│   ├── Assets/              # Images & logos
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript
│   ├── index.html           # Homepage
│   ├── aksi.html           # Main action page
│   └── panduan.html        # Guide page
│
├── .venv/                   # Virtual environment (created by you)
├── .gitignore
└── README.md               # This file
```

## 🛠️ Troubleshooting

### ❌ Error: "python tidak dikenali"

**Solusi:** Install Python atau gunakan `python3` atau `py` sebagai pengganti `python`.

### ❌ Error: "No module named 'flask'"

**Solusi:** Pastikan virtual environment sudah aktif dan jalankan `pip install -r requirements.txt`.

### ❌ Error: "Port 5000 already in use"

**Solusi:**

1. Tutup aplikasi lain yang menggunakan port 5000
2. Atau edit `config.py` dan ubah `PORT = 5000` menjadi port lain (misal: `5001`)

### ❌ Kamera tidak muncul

**Solusi:**

- Pastikan browser memiliki izin akses kamera
- Untuk production, gunakan HTTPS (localhost tidak perlu)
- Chrome/Firefox/Edge: Settings → Privacy → Camera

### ❌ Model tidak terdeteksi

**Solusi:** Pastikan file `Backend-Qoffea/models/best.pt` ada. File ini adalah model YOLO yang sudah ditraining.

## 🔧 Configuration

Edit file `Backend-Qoffea/config.py` untuk mengubah konfigurasi:

```python
# Server settings
HOST = '0.0.0.0'        # Bind ke semua network interfaces
PORT = 5000             # Port number
DEBUG = True            # Debug mode

# Model settings
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence untuk deteksi
```

## 📊 API Endpoints

Jika ingin menggunakan API secara langsung:

| Method | Endpoint                    | Description            |
| ------ | --------------------------- | ---------------------- |
| GET    | `/api/health`               | Check server status    |
| POST   | `/api/upload`               | Upload & analyze image |
| GET    | `/api/report/<id>/download` | Download PDF report    |
| GET    | `/uploads/<filename>`       | Get uploaded image     |
| GET    | `/reports/<filename>`       | Get PDF report         |

**Example API Usage:**

```bash
# Upload image
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "file=@biji_kopi.jpg"

# Download PDF
curl -O http://127.0.0.1:5000/api/report/<analysis_id>/download
```

## 📦 Dependencies

Main libraries yang digunakan:

- **Flask 3.0.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Ultralytics (YOLO)** - AI object detection
- **PyTorch** - Deep learning framework
- **OpenCV** - Image processing
- **Pillow** - Image manipulation
- **ReportLab** - PDF generation
- **NumPy** - Numerical computing

Lihat `Backend-Qoffea/requirements.txt` untuk daftar lengkap.

## 🎓 Model Information

- **Model Type:** YOLOv8 (Ultralytics)
- **Classes:**
  - `coffee-grade-break` (biji cacat/defect)
  - `coffee-grade-good` (biji baik/good)
- **Grading System:**
  - **Grade A:** ≥85% biji baik (Excellent quality)
  - **Grade B:** ≥70% biji baik (Good quality)
  - **Grade C:** <70% biji baik (Fair quality)

## 🌐 Akses dari Perangkat Lain (Network)

Untuk mengakses dari perangkat lain di jaringan yang sama:

1. Cari IP address komputer yang menjalankan server:

   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

2. Catat IPv4 Address (misal: `192.168.1.16`)

3. Dari perangkat lain, akses:
   - http://192.168.1.16:5000/aksi
   - Pastikan firewall mengizinkan koneksi ke port 5000

## 🛑 Menghentikan Server

Untuk menghentikan backend server:

- Tekan `Ctrl + C` di terminal
- Atau tutup terminal/command prompt

## 📝 Development Notes

- Backend menggunakan Flask development server (tidak untuk production)
- Auto-reload enabled: server akan restart otomatis saat code berubah
- Debug mode ON: error messages akan ditampilkan di browser
- Uploaded images & PDF reports tersimpan temporary di folder `uploads/` dan `reports/`

## 🤝 Support

Jika mengalami kendala:

1. Pastikan semua langkah instalasi sudah benar
2. Cek error message di terminal
3. Pastikan Python version ≥ 3.8
4. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 📄 License

Copyright © 2025 QOFFEA Team

---

**Selamat mencoba! ☕🚀**

Untuk pertanyaan atau bantuan, silakan hubungi tim developer.
