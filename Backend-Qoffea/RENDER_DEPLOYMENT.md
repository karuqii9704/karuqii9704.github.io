# Render Deployment Guide for Qoffea

## 🚀 Konfigurasi Render

### 1. **Basic Settings**

- **Name**: `Qoffea` (atau nama lain)
- **Language**: `Python 3`
- **Branch**: `main`
- **Region**: `Singapore (Southeast Asia)` (untuk latency terbaik)

### 2. **Build & Deploy Settings**

#### Root Directory:

```
Backend-Qoffea
```

#### Build Command:

```bash
pip install -r requirements.txt
```

#### Start Command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 3. **Environment Variables**

Tambahkan di Render Dashboard > Environment:

```env
# Flask Configuration
SECRET_KEY=GENERATE_RANDOM_SECRET_KEY_HERE
FLASK_ENV=production
FLASK_DEBUG=0

# Server
HOST=0.0.0.0
PORT=10000

# Hugging Face Model
HF_MODEL_REPO=rakaval/coffea
HF_MODEL_FILE=best.pt
MODEL_CACHE_DIR=/opt/render/project/src/model_cache
CONFIDENCE_THRESHOLD=0.5

# Upload & Reports
UPLOAD_FOLDER=/opt/render/project/src/uploads
REPORT_FOLDER=/opt/render/project/src/reports
MAX_FILE_SIZE=10485760

# CORS (Update setelah deployment)
CORS_ORIGINS=*
```

### 4. **Generate SECRET_KEY**

Gunakan Python untuk generate:

```python
import secrets
print(secrets.token_hex(32))
```

### 5. **Instance Type**

- **Free Tier**: Cukup untuk testing
- **Paid**: Untuk production dengan traffic tinggi

---

## 📝 Checklist Deployment

- [x] Push kode ke GitHub
- [x] Tambahkan `gunicorn` di requirements.txt
- [x] Buat `Procfile`
- [x] Set `DEBUG=False` default
- [ ] Connect Render ke GitHub repo
- [ ] Set Root Directory: `Backend-Qoffea`
- [ ] Set Build Command
- [ ] Set Start Command
- [ ] Tambahkan Environment Variables
- [ ] Deploy!

---

## ⚠️ Important Notes

### Model Download

- Model (40.8MB) akan diunduh saat **first deployment**
- Proses build akan lebih lama di deployment pertama (~2-5 menit)
- Model akan di-cache untuk deployment berikutnya

### Storage

- Render free tier memiliki **ephemeral storage**
- Folder `uploads/` dan `reports/` akan **hilang** setelah redeploy
- Untuk persistent storage, gunakan Render Disks atau external storage (S3, Cloudinary)

### CORS

- Setelah deployment, update `CORS_ORIGINS` dengan domain frontend Anda
- Contoh: `https://yourfrontend.com`

### Timeout

- Start command menggunakan `--timeout 120` untuk AI inference
- Model loading butuh waktu ~30-60 detik

---

## 🔍 Troubleshooting

### Build Fails

1. Check requirements.txt syntax
2. Pastikan Python version compatible
3. Check Render logs

### App Doesn't Start

1. Verify Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
2. Check environment variables
3. Review application logs

### Model Download Fails

1. Check internet connectivity di Render
2. Verify HF_MODEL_REPO dan HF_MODEL_FILE
3. Check Hugging Face repository accessibility

### 502 Bad Gateway

1. App mungkin masih loading model (tunggu ~1 menit)
2. Check logs untuk errors
3. Verify PORT environment variable

---

## 📊 Expected Deployment Time

1. **First Deploy**: 3-5 minutes

   - Install dependencies: ~1-2 min
   - Download model: ~1-2 min
   - Start app: ~30 sec

2. **Subsequent Deploys**: 1-2 minutes
   - Dependencies cached
   - Model might need re-download

---

## 🎯 Post-Deployment

### Test Endpoints:

1. **Health Check**:

   ```
   GET https://your-app.onrender.com/api/health
   ```

2. **Upload Image**:

   ```
   POST https://your-app.onrender.com/api/upload
   ```

3. **Frontend**:
   ```
   https://your-app.onrender.com/index
   ```

---

## 💡 Tips

1. Monitor first deployment logs carefully
2. Test dengan Postman/Thunder Client sebelum frontend
3. Enable "Auto-Deploy" untuk automatic deploys from GitHub
4. Set up health check endpoint monitoring
5. Consider upgrading to paid plan untuk production use

---

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Python on Render: https://render.com/docs/deploy-flask
