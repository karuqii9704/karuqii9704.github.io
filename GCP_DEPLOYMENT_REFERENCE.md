# 🚀 Qoffea - Google Cloud Platform Deployment Reference

**Last Updated:** November 3, 2025  
**Status:** ✅ Production - Fully Operational  
**Project:** Qoffea - Coffee Beans Image Classification with AI

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [GCP Project Details](#gcp-project-details)
- [Deployed Services](#deployed-services)
- [URLs & Access Points](#urls--access-points)
- [Architecture](#architecture)
- [Essential Commands](#essential-commands)
- [Troubleshooting](#troubleshooting)
- [Cost Management](#cost-management)
- [Development Workflow](#development-workflow)

---

## 🎯 Project Overview

**Qoffea** adalah aplikasi AI untuk klasifikasi kualitas biji kopi menggunakan computer vision (YOLO v8).

### Tech Stack:

- **Backend:** Flask 3.0.3 + Python 3.11
- **ML Model:** Ultralytics YOLO v8 (Hugging Face: rakaval/coffea)
- **Frontend:** HTML/CSS/JavaScript (Vanilla)
- **Cloud:** Google Cloud Platform
  - Cloud Run (Backend API)
  - Cloud Storage (Frontend Static Files)
  - Load Balancer + CDN
  - Google-managed SSL Certificate

### Features:

- ✅ Upload gambar dari galeri atau kamera
- ✅ Deteksi biji kopi (good/defect) dengan bounding boxes
- ✅ Grading otomatis (A/B/C/D)
- ✅ Generate PDF report
- ✅ Real-time analysis dengan confidence threshold

---

## 🔧 GCP Project Details

### Project Information

```bash
Project ID: qoffea-backend-7133
Project Number: 493152580351
Region: asia-southeast2 (Jakarta)
Billing Account: 016A1F-33F09A-DD0B1F
Owner: rifqisigwannugraha@gmail.com
```

### Enabled APIs

```bash
# List enabled APIs
gcloud services list --enabled --project=qoffea-backend-7133

# Key APIs:
- run.googleapis.com (Cloud Run)
- storage.googleapis.com (Cloud Storage)
- cloudbuild.googleapis.com (Cloud Build)
- containerregistry.googleapis.com (Container Registry)
- compute.googleapis.com (Compute Engine)
```

### IAM & Service Accounts

```bash
# Main Service Account
493152580351-compute@developer.gserviceaccount.com

# Roles:
- roles/storage.admin (for Cloud Build to push images)
- roles/run.admin (for Cloud Run deployments)

# Check service account
gcloud iam service-accounts list --project=qoffea-backend-7133
```

---

## 🌐 Deployed Services

### 1️⃣ Backend (Cloud Run)

**Service Details:**

```yaml
Service Name: qoffea-backend
Region: asia-southeast2
URL: https://qoffea-backend-c26brvbilq-et.a.run.app
Platform: managed
Container: asia-southeast2-docker.pkg.dev/qoffea-backend-7133/cloud-run-source-deploy/qoffea-backend
```

**Resource Configuration:**

```yaml
Memory: 4Gi
CPU: 2
Timeout: 300s
Max Instances: 3
Min Instances: 0 (scales to zero)
Concurrency: 80 (default)
```

**Environment Variables:**

```bash
FLASK_ENV=production
HF_MODEL_REPO=rakaval/coffea
HF_MODEL_FILE=best.pt
CONFIDENCE_THRESHOLD=0.5
```

**Check Service:**

```bash
# Get service details
gcloud run services describe qoffea-backend \
  --region=asia-southeast2 \
  --project=qoffea-backend-7133

# View logs
gcloud run services logs read qoffea-backend \
  --region=asia-southeast2 \
  --project=qoffea-backend-7133 \
  --limit=50

# Get latest revision
gcloud run revisions list \
  --service=qoffea-backend \
  --region=asia-southeast2 \
  --project=qoffea-backend-7133
```

### 2️⃣ Frontend (Cloud Storage + Load Balancer)

**Storage Bucket:**

```yaml
Bucket Name: qoffea-frontend-7133
Location: asia-southeast2
Storage Class: Standard
Public Access: Enabled (allUsers)
Website Configuration: Enabled (index.html)
```

**Backend Bucket:**

```yaml
Backend Name: qoffea-frontend-backend
CDN Enabled: Yes
Cache Mode: CACHE_ALL_STATIC
```

**Load Balancer:**

```yaml
Name: qoffea-lb
Type: HTTPS Load Balancer
Static IP: 34.49.190.69
Domain: 34-49-190-69.nip.io
SSL Certificate: qoffea-ssl-cert (Google-managed)
Status: ACTIVE
```

**Check Frontend:**

```bash
# List bucket contents
gcloud storage ls gs://qoffea-frontend-7133/ --recursive

# Check bucket details
gcloud storage buckets describe gs://qoffea-frontend-7133

# View load balancer
gcloud compute forwarding-rules list --global

# Check SSL certificate
gcloud compute ssl-certificates describe qoffea-ssl-cert --global
```

---

## 🔗 URLs & Access Points

### Production URLs

```bash
# Frontend (Load Balancer)
HTTP:  http://34-49-190-69.nip.io
HTTPS: https://34-49-190-69.nip.io

# Direct Cloud Storage (Fallback)
https://storage.googleapis.com/qoffea-frontend-7133/index.html
https://storage.googleapis.com/qoffea-frontend-7133/aksi.html
https://storage.googleapis.com/qoffea-frontend-7133/panduan.html

# Backend API (Cloud Run)
https://qoffea-backend-c26brvbilq-et.a.run.app

# API Endpoints
https://qoffea-backend-c26brvbilq-et.a.run.app/api/health
https://qoffea-backend-c26brvbilq-et.a.run.app/api/upload
https://qoffea-backend-c26brvbilq-et.a.run.app/uploads/{filename}
https://qoffea-backend-c26brvbilq-et.a.run.app/api/report/{id}/download
```

### Static IP

```bash
Name: qoffea-static-ip
Address: 34.49.190.69
Type: EXTERNAL
Tier: PREMIUM
Region: Global
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTPS (SSL Certificate)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           Google Cloud Load Balancer (Global)               │
│                    IP: 34.49.190.69                         │
│                 Domain: 34-49-190-69.nip.io                 │
└────────┬────────────────────────────────────────────┬───────┘
         │                                            │
         │ Static Files                               │ API Requests
         ▼                                            ▼
┌─────────────────────┐                    ┌──────────────────────┐
│  Cloud Storage      │                    │    Cloud Run         │
│  (Frontend)         │                    │    (Backend)         │
│                     │                    │                      │
│  - HTML/CSS/JS      │                    │  - Flask API         │
│  - Assets/Images    │                    │  - YOLO Model        │
│  - CDN Enabled      │                    │  - Image Processing  │
│                     │                    │  - PDF Generation    │
│  Bucket:            │                    │                      │
│  qoffea-frontend-   │                    │  Memory: 4Gi         │
│  7133               │                    │  CPU: 2              │
└─────────────────────┘                    └──────────┬───────────┘
                                                      │
                                                      │ Model Download
                                                      ▼
                                           ┌──────────────────────┐
                                           │   Hugging Face Hub   │
                                           │   rakaval/coffea     │
                                           │   Model: best.pt     │
                                           └──────────────────────┘
```

---

## ⚡ Essential Commands

### 🔐 Authentication & Setup

```bash
# Login to Google Cloud
gcloud auth login

# Set default project
gcloud config set project qoffea-backend-7133

# Set default region
gcloud config set run/region asia-southeast2

# Verify configuration
gcloud config list
```

### 🚀 Backend Deployment (Cloud Run)

```bash
# Navigate to backend directory
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Backend-Qoffea"

# Deploy with all configurations
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

# Update environment variable only
gcloud run services update qoffea-backend \
  --region=asia-southeast2 \
  --update-env-vars CONFIDENCE_THRESHOLD=0.6

# Scale configuration
gcloud run services update qoffea-backend \
  --region=asia-southeast2 \
  --min-instances=0 \
  --max-instances=5

# View service URL
gcloud run services describe qoffea-backend \
  --region=asia-southeast2 \
  --format='value(status.url)'
```

### 📦 Frontend Deployment (Cloud Storage)

```bash
# Upload all frontend files
gcloud storage cp -r "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea\*" \
  gs://qoffea-frontend-7133/

# Upload specific files
gcloud storage cp "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea\index.html" \
  gs://qoffea-frontend-7133/

gcloud storage cp "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea\aksi.html" \
  gs://qoffea-frontend-7133/

gcloud storage cp "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea\js\app.js" \
  gs://qoffea-frontend-7133/js/

# Upload with cache control (no cache for development)
gcloud storage cp "Frontend-Qoffea\js\app.js" \
  gs://qoffea-frontend-7133/js/ \
  --cache-control="no-cache,max-age=0"

# Set cache control for existing file
gcloud storage objects update gs://qoffea-frontend-7133/js/app.js \
  --cache-control="no-cache,max-age=0"

# Make bucket public (if needed)
gcloud storage buckets add-iam-policy-binding gs://qoffea-frontend-7133 \
  --member=allUsers \
  --role=roles/storage.objectViewer
```

### 📊 Monitoring & Logs

```bash
# View Cloud Run logs (live)
gcloud run services logs tail qoffea-backend \
  --region=asia-southeast2

# View specific number of log entries
gcloud run services logs read qoffea-backend \
  --region=asia-southeast2 \
  --limit=100

# View build logs
gcloud builds list --limit=5
gcloud builds log <BUILD_ID> --region=asia-southeast2

# Monitor service metrics (opens in browser)
gcloud run services browse qoffea-backend --region=asia-southeast2

# Check service status
gcloud run services list --platform=managed
```

### 🔍 Debugging & Testing

```bash
# Test backend health endpoint
Invoke-RestMethod -Uri "https://qoffea-backend-c26brvbilq-et.a.run.app/api/health" | ConvertTo-Json

# Test with curl (PowerShell)
curl https://qoffea-backend-c26brvbilq-et.a.run.app/api/health

# Check frontend access
Invoke-WebRequest -Uri "https://34-49-190-69.nip.io/aksi.html" -UseBasicParsing

# View container image
gcloud container images list --repository=asia-southeast2-docker.pkg.dev/qoffea-backend-7133/cloud-run-source-deploy

# SSH into Cloud Shell (for debugging)
gcloud cloud-shell ssh
```

### 🔐 SSL Certificate Management

```bash
# Check SSL certificate status
gcloud compute ssl-certificates describe qoffea-ssl-cert --global

# Check status only
gcloud compute ssl-certificates describe qoffea-ssl-cert \
  --global \
  --format="value(managed.status)"

# List all SSL certificates
gcloud compute ssl-certificates list

# Create new SSL certificate (if needed)
gcloud compute ssl-certificates create qoffea-ssl-cert \
  --domains=34-49-190-69.nip.io \
  --global
```

### 🌐 Load Balancer Management

```bash
# List forwarding rules
gcloud compute forwarding-rules list --global

# Describe HTTPS forwarding rule
gcloud compute forwarding-rules describe qoffea-https-rule --global

# List URL maps
gcloud compute url-maps list

# List backend buckets
gcloud compute backend-buckets list

# Update backend bucket
gcloud compute backend-buckets update qoffea-frontend-backend \
  --enable-cdn
```

### 💰 Cost Management

```bash
# View current billing
gcloud billing accounts list

# Check project billing
gcloud billing projects describe qoffea-backend-7133

# Set budget alerts (via Console recommended)
# https://console.cloud.google.com/billing/budgets

# Estimate costs
gcloud run services describe qoffea-backend \
  --region=asia-southeast2 \
  --format="table(status.url,spec.template.spec.containers[0].resources)"
```

### 🗑️ Cleanup Commands (Use with Caution!)

```bash
# Delete Cloud Run service
gcloud run services delete qoffea-backend --region=asia-southeast2

# Delete Cloud Storage bucket
gcloud storage rm -r gs://qoffea-frontend-7133

# Delete SSL certificate
gcloud compute ssl-certificates delete qoffea-ssl-cert --global

# Delete load balancer components
gcloud compute forwarding-rules delete qoffea-https-rule --global
gcloud compute target-https-proxies delete qoffea-https-proxy --global
gcloud compute url-maps delete qoffea-url-map --global
gcloud compute backend-buckets delete qoffea-frontend-backend --global

# Release static IP
gcloud compute addresses delete qoffea-static-ip --global

# Delete entire project (DANGER!)
gcloud projects delete qoffea-backend-7133
```

---

## 🐛 Troubleshooting

### Problem: Backend returns 500 error

```bash
# Check logs for errors
gcloud run services logs read qoffea-backend \
  --region=asia-southeast2 \
  --limit=50

# Common issues:
# 1. Model download failed (Hugging Face)
# 2. Memory limit exceeded (increase to 8Gi)
# 3. Timeout (increase timeout)

# Solution: Increase resources
gcloud run services update qoffea-backend \
  --region=asia-southeast2 \
  --memory=8Gi \
  --timeout=600
```

### Problem: Frontend not updating (browser cache)

```bash
# Set no-cache headers
gcloud storage objects update gs://qoffea-frontend-7133/js/app.js \
  --cache-control="no-cache,max-age=0"

# Or add version query string in HTML
<script src="js/app.js?v=20251103"></script>

# User solution: Hard refresh (Ctrl + Shift + R)
```

### Problem: SSL certificate provisioning stuck

```bash
# Check status
gcloud compute ssl-certificates describe qoffea-ssl-cert --global

# If stuck > 60 minutes, delete and recreate
gcloud compute ssl-certificates delete qoffea-ssl-cert --global
gcloud compute ssl-certificates create qoffea-ssl-cert \
  --domains=34-49-190-69.nip.io \
  --global

# Update HTTPS proxy
gcloud compute target-https-proxies update qoffea-https-proxy \
  --ssl-certificates=qoffea-ssl-cert \
  --global
```

### Problem: CORS errors

```bash
# Backend handles CORS via Flask-CORS
# Check config.py: CORS_ORIGINS = '*'

# Verify in logs
gcloud run services logs read qoffea-backend \
  --region=asia-southeast2 | grep -i "cors"
```

### Problem: Image upload fails

```bash
# Check if model is loaded
curl https://qoffea-backend-c26brvbilq-et.a.run.app/api/health

# Check file size limit (10MB default)
# Increase in config.py: MAX_FILE_SIZE

# Check allowed extensions
# config.py: ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
```

### Problem: Container build fails

```bash
# Check build logs
gcloud builds list --limit=5
gcloud builds log <BUILD_ID> --region=asia-southeast2

# Common issues:
# 1. Dockerfile errors (missing dependencies)
# 2. Build timeout (increase timeout)
# 3. Permission denied (check IAM)

# Manual build test locally
docker build -t qoffea-backend .
docker run -p 5000:5000 qoffea-backend
```

---

## 💵 Cost Management

### Current Configuration Costs (Estimated)

**Cloud Run (Backend):**

```
Memory: 4Gi
CPU: 2 vCPU
Requests: ~100/month (estimated)

Cost per month (estimate):
- Compute: $15-30/month (depends on usage)
- Networking: $1-5/month
- Total: ~$20-35/month

Free tier: 2M requests, 360,000 GB-seconds, 180,000 vCPU-seconds per month
```

**Cloud Storage (Frontend):**

```
Storage: ~50MB
Requests: ~1000/month

Cost per month:
- Storage: <$0.50/month
- Operations: <$0.50/month
- Total: ~$1/month

Free tier: 5GB storage, 5,000 Class A operations per month
```

**Load Balancer + SSL:**

```
Static IP: $0 (while in use)
Forwarding rules: ~$18/month
Data processing: $0.008-$0.025/GB
SSL certificate: Free (Google-managed)

Total: ~$20-30/month
```

**Total Estimated Cost: $40-70/month**

### Cost Optimization Tips

```bash
# 1. Scale to zero when not in use
gcloud run services update qoffea-backend \
  --region=asia-southeast2 \
  --min-instances=0

# 2. Reduce max instances
gcloud run services update qoffea-backend \
  --region=asia-southeast2 \
  --max-instances=2

# 3. Set budget alerts
# Go to: https://console.cloud.google.com/billing/budgets
# Set alert at $50/month

# 4. Monitor usage
gcloud logging read "resource.type=cloud_run_revision" \
  --limit=10 \
  --format=json

# 5. Use Cloud Storage directly (skip Load Balancer for testing)
https://storage.googleapis.com/qoffea-frontend-7133/aksi.html
```

---

## 🔄 Development Workflow

### Making Changes to Backend

```bash
# 1. Make changes locally
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Backend-Qoffea"
# Edit files...

# 2. Test locally (optional)
python app.py

# 3. Commit changes
git add .
git commit -m "feat: Your changes description"

# 4. Deploy to Cloud Run
gcloud run deploy qoffea-backend \
  --source . \
  --region=asia-southeast2 \
  --platform managed

# 5. Verify deployment
curl https://qoffea-backend-c26brvbilq-et.a.run.app/api/health

# 6. Check logs if issues
gcloud run services logs read qoffea-backend --region=asia-southeast2 --limit=20
```

### Making Changes to Frontend

```bash
# 1. Make changes locally
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea"
# Edit HTML/CSS/JS...

# 2. Update cache busting version in HTML (if JS changed)
# aksi.html: <script src="js/app.js?v=20251104"></script>

# 3. Commit changes
git add .
git commit -m "feat: Your changes description"

# 4. Deploy to Cloud Storage
gcloud storage cp -r * gs://qoffea-frontend-7133/

# 5. Set no-cache for JS files (during development)
gcloud storage objects update gs://qoffea-frontend-7133/js/app.js \
  --cache-control="no-cache,max-age=0"

# 6. Test in browser with hard refresh (Ctrl + Shift + R)
```

### Updating API Base URL

If backend URL changes, update in frontend:

```javascript
// File: Frontend-Qoffea/js/app.js
const API_BASE_URL = "https://qoffea-backend-c26brvbilq-et.a.run.app/api";
```

Then redeploy frontend:

```bash
gcloud storage cp "Frontend-Qoffea/js/app.js" gs://qoffea-frontend-7133/js/
```

---

## 📱 Quick Reference Card

### Most Used Commands

```bash
# Deploy backend
gcloud run deploy qoffea-backend --source . --region=asia-southeast2

# Deploy frontend
gcloud storage cp -r Frontend-Qoffea/* gs://qoffea-frontend-7133/

# View logs
gcloud run services logs tail qoffea-backend --region=asia-southeast2

# Health check
curl https://qoffea-backend-c26brvbilq-et.a.run.app/api/health

# Check SSL
gcloud compute ssl-certificates describe qoffea-ssl-cert --global --format="value(managed.status)"

# Set project
gcloud config set project qoffea-backend-7133
```

### Important URLs (Copy-Paste Ready)

```
Production:
https://34-49-190-69.nip.io/aksi.html

Backend API:
https://qoffea-backend-c26brvbilq-et.a.run.app/api/health

GCP Console:
https://console.cloud.google.com/run?project=qoffea-backend-7133

Cloud Storage:
https://console.cloud.google.com/storage/browser/qoffea-frontend-7133

Load Balancer:
https://console.cloud.google.com/net-services/loadbalancing/loadBalancers/list?project=qoffea-backend-7133
```

---

## 🤖 AI Assistant Notes

**For Copilot / AI Assistants:**

When user asks about Qoffea deployment:

1. **Project Context:** This is a production Flask + YOLO AI application deployed on GCP
2. **Key Facts:**

   - Backend: Cloud Run (stateless, ephemeral storage)
   - Frontend: Cloud Storage + Load Balancer
   - No database (by design - privacy focused)
   - Uploaded images are temporary (container lifetime only)

3. **Common Issues:**

   - Browser cache → Solution: Hard refresh (Ctrl+Shift+R)
   - Image not showing → Check API_BASE_URL in app.js
   - Backend timeout → Increase timeout or memory
   - SSL provisioning → Wait 15-60 minutes

4. **Don't suggest:**

   - Persistent storage for uploads (intentional design)
   - Database setup (not in scope)
   - Changing to other cloud providers (already GCP)

5. **Always check:**
   - Is gcloud authenticated?
   - Is correct project set?
   - Are environment variables correct?
   - Is cache busting needed?

---

## 📚 Additional Resources

- **GCP Cloud Run Documentation:** https://cloud.google.com/run/docs
- **GCP Cloud Storage:** https://cloud.google.com/storage/docs
- **Hugging Face Hub:** https://huggingface.co/rakaval/coffea
- **Ultralytics YOLO:** https://docs.ultralytics.com/
- **Flask Documentation:** https://flask.palletsprojects.com/

---

## 📝 Change Log

### November 3, 2025

- ✅ Initial deployment to Google Cloud
- ✅ Backend deployed to Cloud Run with YOLO model
- ✅ Frontend deployed to Cloud Storage
- ✅ Load Balancer + SSL certificate configured
- ✅ Fixed browser cache issue with cache busting
- ✅ Fixed API_BASE_URL for production
- ✅ All services tested and operational

---

## 👥 Team & Support

**Owner:** rifqisigwannugraha@gmail.com  
**Project:** Coffee Beans Image Classification  
**Repository:** karuqii9704/karuqii9704.github.io  
**Branch:** main

---

**🎉 Deployment Status: PRODUCTION - FULLY OPERATIONAL ✅**

Last verified: November 3, 2025
