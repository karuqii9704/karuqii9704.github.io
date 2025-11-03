# 🚀 Quick Start Guide - QOFFEA

Panduan cepat untuk menjalankan aplikasi Qoffea di perangkat baru.

## ⚡ Langkah Cepat (5 Menit)

### 1. Pastikan Python Terinstall

```bash
python --version
# Harus Python 3.8 atau lebih tinggi
```

### 2. Setup Virtual Environment

```bash
# Di root folder Qoffea
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
cd Backend-Qoffea
pip install -r requirements.txt
```

### 4. Jalankan Server

```bash
python app.py
```

### 5. Buka Browser

```
http://127.0.0.1:5000/aksi
```

## 🎯 URL Penting

| Halaman            | URL                           |
| ------------------ | ----------------------------- |
| Analisis Biji Kopi | http://127.0.0.1:5000/aksi    |
| Homepage           | http://127.0.0.1:5000         |
| Panduan            | http://127.0.0.1:5000/panduan |

## 📝 Perintah Lengkap (Copy-Paste)

**Windows PowerShell:**

```powershell
# 1. Buat dan aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
cd Backend-Qoffea
pip install -r requirements.txt

# 3. Jalankan server
python app.py

# Server akan berjalan di http://127.0.0.1:5000
# Buka browser dan akses http://127.0.0.1:5000/aksi
```

**Linux/Mac Terminal:**

```bash
# 1. Buat dan aktifkan virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
cd Backend-Qoffea
pip install -r requirements.txt

# 3. Jalankan server
python app.py

# Server akan berjalan di http://127.0.0.1:5000
# Buka browser dan akses http://127.0.0.1:5000/aksi
```

## ⚠️ Troubleshooting Cepat

**Error: "Scripts is disabled"** (Windows)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Error: "python tidak dikenali"**

- Ganti `python` dengan `python3` atau `py`
- Atau install Python dari python.org

**Error: "Port 5000 already in use"**

- Tutup aplikasi yang menggunakan port 5000
- Atau ganti port di `config.py`

**Kamera tidak berfungsi**

- Izinkan akses kamera di browser
- Chrome: chrome://settings/content/camera

## 🌐 Akses dari HP/Laptop Lain

1. Cek IP komputer server:

   ```bash
   # Windows
   ipconfig

   # Linux/Mac
   ifconfig
   ```

2. Catat IPv4 (contoh: 192.168.1.16)

3. Di perangkat lain, buka:
   ```
   http://192.168.1.16:5000/aksi
   ```

## 📞 Butuh Bantuan?

Lihat **README.md** untuk dokumentasi lengkap!
