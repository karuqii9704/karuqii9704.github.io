# 🚀 Google Cloud Deployment Guide - Qoffea Backend

Panduan lengkap untuk deploy Qoffea Backend ke Google Cloud Platform.

## 📋 Prerequisites

1. **Google Cloud Account** - Buat di [cloud.google.com](https://cloud.google.com)
2. **Project GCP** - Buat project baru di GCP Console
3. **Billing Enabled** - Aktifkan billing untuk project Anda
4. **Google Cloud CLI** - Install [gcloud CLI](https://cloud.google.com/sdk/docs/install)

## 🛠️ Setup Awal

### 1. Install Google Cloud CLI

**Windows:**
```powershell
# Download dari: https://cloud.google.com/sdk/docs/install
# Atau gunakan chocolatey:
choco install gcloudsdk
```

**Verifikasi instalasi:**
```powershell
gcloud --version
```

### 2. Login dan Setup Project

```powershell
# Login ke Google Cloud
gcloud auth login

# Set project ID (ganti dengan project ID Anda)
gcloud config set project YOUR_PROJECT_ID

# Verifikasi project
gcloud config get-value project
```

### 3. Enable APIs yang Diperlukan

```powershell
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API (untuk CI/CD)
gcloud services enable cloudbuild.googleapis.com

# Enable Artifact Registry (opsional, alternatif Container Registry)
gcloud services enable artifactregistry.googleapis.com
```

## 🎯 Opsi Deployment

### **Opsi 1: Google Cloud Run (RECOMMENDED)** ⭐

Cloud Run adalah serverless platform yang cocok untuk aplikasi ML seperti Qoffea.

#### Keuntungan:
- ✅ Auto-scaling (scale to zero)
- ✅ Pay per use
- ✅ Support Docker container
- ✅ Cocok untuk ML workloads
- ✅ Mudah di-setup

#### Deploy ke Cloud Run:

```powershell
# 1. Set region (pilih yang terdekat)
gcloud config set run/region asia-southeast2  # Jakarta
# atau: us-central1, europe-west1, asia-east1

# 2. Build dan deploy dalam satu perintah
gcloud run deploy qoffea-backend \
  --source . \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 3 \
  --set-env-vars "FLASK_ENV=production,HF_MODEL_REPO=rakaval/coffea,HF_MODEL_FILE=best.pt,CONFIDENCE_THRESHOLD=0.5"
```

**Atau build Docker image terlebih dahulu:**

```powershell
# 1. Build Docker image locally
docker build -t gcr.io/YOUR_PROJECT_ID/qoffea-backend .

# 2. Push ke Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/qoffea-backend

# 3. Deploy ke Cloud Run
gcloud run deploy qoffea-backend \
  --image gcr.io/YOUR_PROJECT_ID/qoffea-backend \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2
```

### **Opsi 2: Google App Engine Flexible**

App Engine Flexible juga support ML models, tapi lebih mahal dan lebih lambat deploy.

```powershell
# Deploy dengan app.yaml
gcloud app deploy

# Set traffic ke versi baru
gcloud app deploy --promote
```

## 🔧 Environment Variables

Set environment variables di Cloud Run:

```powershell
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --set-env-vars "
    FLASK_ENV=production,
    FLASK_DEBUG=0,
    HF_MODEL_REPO=rakaval/coffea,
    HF_MODEL_FILE=best.pt,
    MODEL_CACHE_DIR=/tmp/model_cache,
    CONFIDENCE_THRESHOLD=0.5,
    MAX_FILE_SIZE=10485760,
    SECRET_KEY=your-secure-secret-key-here
  "
```

Atau gunakan secrets manager (lebih aman):

```powershell
# Buat secret
echo -n "your-secret-key" | gcloud secrets create flask-secret-key --data-file=-

# Gunakan secret di Cloud Run
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --update-secrets SECRET_KEY=flask-secret-key:latest
```

## 📊 Monitoring & Logs

### Lihat Logs:
```powershell
# Real-time logs
gcloud run services logs tail qoffea-backend --region asia-southeast2

# Logs di Cloud Console
# https://console.cloud.google.com/logs
```

### Monitoring:
```powershell
# Lihat service details
gcloud run services describe qoffea-backend --region asia-southeast2

# Monitoring dashboard
# https://console.cloud.google.com/run
```

## 🔒 Security & Authentication

### Allow Unauthenticated Access (Public API):
```powershell
gcloud run services add-iam-policy-binding qoffea-backend \
  --region asia-southeast2 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

### Require Authentication:
```powershell
gcloud run services remove-iam-policy-binding qoffea-backend \
  --region asia-southeast2 \
  --member="allUsers" \
  --role="roles/run.invoker"
```

## 💰 Cost Optimization

### Tips untuk menghemat biaya:

1. **Set max instances**:
```powershell
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --max-instances 3
```

2. **Set min instances** (0 untuk scale to zero):
```powershell
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --min-instances 0
```

3. **Optimize memory**:
```powershell
# Start dengan 2Gi, naikkan jika perlu
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --memory 2Gi
```

## 🌐 Custom Domain

### Setup Custom Domain:

1. Buka Cloud Run Console
2. Pilih service `qoffea-backend`
3. Klik "Manage Custom Domains"
4. Tambah domain dan ikuti instruksi DNS

Atau via CLI:
```powershell
gcloud run domain-mappings create \
  --service qoffea-backend \
  --domain api.yourdomain.com \
  --region asia-southeast2
```

## 🔄 CI/CD dengan Cloud Build

Setup automatic deployment dari GitHub:

1. **Connect Repository**:
   - Buka Cloud Build Console
   - Klik "Triggers"
   - Connect ke GitHub repository

2. **Create Trigger**:
```powershell
gcloud builds triggers create github \
  --repo-name=karuqii9704.github.io \
  --repo-owner=karuqii9704 \
  --branch-pattern="^main$" \
  --build-config=Backend-Qoffea/cloudbuild.yaml
```

Setiap push ke branch `main` akan otomatis deploy!

## 🧪 Testing Deployment

Setelah deploy, test API:

```powershell
# Get service URL
$SERVICE_URL = gcloud run services describe qoffea-backend --region asia-southeast2 --format 'value(status.url)'

# Test health endpoint
curl "$SERVICE_URL/api/health"

# Test upload (Windows PowerShell)
$response = Invoke-RestMethod -Uri "$SERVICE_URL/api/upload" -Method Post -ContentType "multipart/form-data" -Body @{file=Get-Item "path/to/image.jpg"}
echo $response
```

## 📱 Update Frontend

Update URL backend di `Frontend-Qoffea/js/app.js`:

```javascript
// Ganti dengan URL Cloud Run Anda
const API_BASE_URL = 'https://qoffea-backend-xxxxx-xx.a.run.app';
```

## 🚨 Troubleshooting

### Issue: Container fails to start
```powershell
# Check logs
gcloud run services logs tail qoffea-backend --region asia-southeast2

# Check service status
gcloud run services describe qoffea-backend --region asia-southeast2
```

### Issue: Out of memory
```powershell
# Increase memory
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --memory 8Gi
```

### Issue: Timeout
```powershell
# Increase timeout (max 3600s)
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --timeout 600
```

### Issue: Model download fails
- Check Hugging Face model repository accessible
- Verify environment variables set correctly
- Check internet connectivity from Cloud Run

## 📚 Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)

## 💡 Best Practices

1. ✅ Use Cloud Run untuk production (bukan App Engine)
2. ✅ Set proper memory limits (4Gi recommended)
3. ✅ Enable monitoring dan alerting
4. ✅ Use secrets manager untuk sensitive data
5. ✅ Set max instances untuk cost control
6. ✅ Use Cloud CDN untuk static files
7. ✅ Regular backup untuk user uploads
8. ✅ Monitor costs di Billing console

## 🎉 Quick Start Summary

```powershell
# 1. Login
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Enable APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com

# 4. Deploy!
cd Backend-Qoffea
gcloud run deploy qoffea-backend \
  --source . \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2

# 5. Get URL
gcloud run services describe qoffea-backend --region asia-southeast2 --format 'value(status.url)'
```

Selamat! Aplikasi Qoffea Anda sekarang berjalan di Google Cloud! 🚀
