# 📊 Qoffea - Monitoring & Controlling Guide

Panduan lengkap untuk monitoring, controlling, dan maintenance aplikasi Qoffea yang di-deploy di Google Cloud Platform.

## 🌐 URL Aplikasi

### Production URLs
- **Backend API:** `https://qoffea-backend-c26brvbilq-et.a.run.app`
- **Frontend:** `https://storage.googleapis.com/qoffea-frontend-7133/index.html`
- **Project ID:** `qoffea-backend-7133`
- **Region:** `asia-southeast2` (Jakarta)

---

## 📱 Quick Access Links

### Google Cloud Console
```
# Project Dashboard
https://console.cloud.google.com/home/dashboard?project=qoffea-backend-7133

# Cloud Run (Backend)
https://console.cloud.google.com/run?project=qoffea-backend-7133

# Cloud Storage (Frontend)
https://console.cloud.google.com/storage/browser/qoffea-frontend-7133?project=qoffea-backend-7133

# Cloud Build
https://console.cloud.google.com/cloud-build/builds?project=qoffea-backend-7133

# Logs Explorer
https://console.cloud.google.com/logs?project=qoffea-backend-7133

# Monitoring Dashboard
https://console.cloud.google.com/monitoring?project=qoffea-backend-7133

# Billing
https://console.cloud.google.com/billing?project=qoffea-backend-7133
```

---

## 🔍 Monitoring Backend (Cloud Run)

### 1. Health Check
Test apakah backend masih running:

```powershell
# Test via PowerShell
Invoke-RestMethod -Uri "https://qoffea-backend-c26brvbilq-et.a.run.app/api/health"

# Expected Response:
# {
#   "status": "healthy",
#   "model_loaded": true,
#   "classes": {
#     "0": "coffee-grade-break",
#     "1": "coffee-grade-good"
#   }
# }
```

### 2. View Real-time Logs

```powershell
# View logs via CLI
gcloud run services logs tail qoffea-backend --region asia-southeast2

# View logs dengan filter
gcloud run services logs tail qoffea-backend \
  --region asia-southeast2 \
  --filter="severity>=ERROR"

# View logs dalam 1 jam terakhir
gcloud run services logs read qoffea-backend \
  --region asia-southeast2 \
  --limit=50
```

### 3. Service Status & Metrics

```powershell
# Get service details
gcloud run services describe qoffea-backend --region asia-southeast2

# Get service URL
gcloud run services describe qoffea-backend \
  --region asia-southeast2 \
  --format="value(status.url)"

# List all revisions
gcloud run revisions list \
  --service qoffea-backend \
  --region asia-southeast2
```

### 4. Metrics Dashboard

**Via Web Console:**
1. Buka https://console.cloud.google.com/run/detail/asia-southeast2/qoffea-backend/metrics?project=qoffea-backend-7133
2. Lihat metrics:
   - **Request count** - Jumlah request per menit
   - **Request latency** - Response time
   - **Container CPU utilization** - Penggunaan CPU
   - **Container memory utilization** - Penggunaan memory
   - **Container instance count** - Jumlah instances running

**Key Metrics to Monitor:**
- ⚠️ **Request latency > 5s** - Backend lambat, perlu optimasi
- ⚠️ **Memory usage > 90%** - Risiko out of memory, perlu tambah memory
- ⚠️ **Error rate > 5%** - Ada masalah di aplikasi, cek logs
- ⚠️ **Container startup latency > 30s** - Model loading lambat

---

## 🗂️ Monitoring Frontend (Cloud Storage)

### 1. Check Files

```powershell
# List semua files di bucket
gcloud storage ls gs://qoffea-frontend-7133/

# List dengan details
gcloud storage ls -l gs://qoffea-frontend-7133/

# Check specific file
gcloud storage ls gs://qoffea-frontend-7133/index.html
```

### 2. Test Frontend Access

```powershell
# Test homepage
Invoke-WebRequest -Uri "https://storage.googleapis.com/qoffea-frontend-7133/index.html"

# Test aksi page
Invoke-WebRequest -Uri "https://storage.googleapis.com/qoffea-frontend-7133/aksi.html"

# Expected: StatusCode 200
```

### 3. View Storage Metrics

**Via Web Console:**
1. Buka https://console.cloud.google.com/storage/browser/qoffea-frontend-7133?project=qoffea-backend-7133
2. Klik tab "Observability"
3. Lihat:
   - **Total storage** - Ukuran total files
   - **Number of objects** - Jumlah files
   - **Request metrics** - Jumlah request
   - **Bandwidth** - Data transfer

---

## 🔧 Controlling & Management

### Backend Management

#### 1. Update Environment Variables

```powershell
# Update confidence threshold
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --update-env-vars CONFIDENCE_THRESHOLD=0.6

# Update multiple env vars
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --set-env-vars "FLASK_ENV=production,CONFIDENCE_THRESHOLD=0.5"

# View current env vars
gcloud run services describe qoffea-backend \
  --region asia-southeast2 \
  --format="value(spec.template.spec.containers[0].env)"
```

#### 2. Scale Backend

```powershell
# Set minimum instances (untuk reduce cold start)
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --min-instances 1

# Set maximum instances (untuk control cost)
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --max-instances 5

# Update memory
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --memory 8Gi

# Update CPU
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --cpu 4
```

#### 3. Update Backend Code

```powershell
# Deploy update dari source code
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Backend-Qoffea"

gcloud run deploy qoffea-backend \
  --source . \
  --platform managed \
  --region asia-southeast2
```

#### 4. Rollback ke Versi Sebelumnya

```powershell
# List revisions
gcloud run revisions list \
  --service qoffea-backend \
  --region asia-southeast2

# Rollback to specific revision
gcloud run services update-traffic qoffea-backend \
  --region asia-southeast2 \
  --to-revisions REVISION_NAME=100
```

#### 5. Stop/Delete Service

```powershell
# Delete service (stop charging)
gcloud run services delete qoffea-backend --region asia-southeast2

# Confirm: Y
```

### Frontend Management

#### 1. Update Frontend Files

```powershell
# Upload updated files
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea"

# Upload semua files
gcloud storage cp -r . gs://qoffea-frontend-7133/

# Upload specific file
gcloud storage cp aksi.html gs://qoffea-frontend-7133/aksi.html

# Upload dengan cache control
gcloud storage cp -r . gs://qoffea-frontend-7133/ \
  --cache-control="public, max-age=3600"
```

#### 2. Delete Files

```powershell
# Delete specific file
gcloud storage rm gs://qoffea-frontend-7133/old-file.html

# Delete folder
gcloud storage rm -r gs://qoffea-frontend-7133/old-folder/
```

#### 3. Set Cache Control

```powershell
# Set cache untuk CSS/JS (1 hour)
gcloud storage objects update gs://qoffea-frontend-7133/css/*.css \
  --cache-control="public, max-age=3600"

gcloud storage objects update gs://qoffea-frontend-7133/js/*.js \
  --cache-control="public, max-age=3600"

# No cache untuk HTML (immediate updates)
gcloud storage objects update gs://qoffea-frontend-7133/*.html \
  --cache-control="no-cache"
```

---

## 📈 Monitoring Best Practices

### 1. Set Up Alerts

**Via Web Console:**
1. Buka https://console.cloud.google.com/monitoring/alerting?project=qoffea-backend-7133
2. Click "Create Policy"
3. Setup alerts untuk:
   - High error rate (> 5%)
   - High latency (> 5s)
   - High memory usage (> 90%)
   - Budget alerts (over $50/month)

### 2. Daily Monitoring Checklist

```powershell
# 1. Check backend health
Invoke-RestMethod -Uri "https://qoffea-backend-c26brvbilq-et.a.run.app/api/health"

# 2. Check recent errors
gcloud run services logs read qoffea-backend \
  --region asia-southeast2 \
  --filter="severity>=ERROR" \
  --limit=10

# 3. Check service status
gcloud run services describe qoffea-backend --region asia-southeast2

# 4. Check frontend access
Invoke-WebRequest -Uri "https://storage.googleapis.com/qoffea-frontend-7133/index.html"
```

### 3. Weekly Review

**Check these metrics weekly:**
1. **Request count trends** - Are users increasing?
2. **Error rate** - Any recurring errors?
3. **Cost trends** - Billing amount normal?
4. **Performance** - Latency acceptable?

**Via Console:**
```
https://console.cloud.google.com/run/detail/asia-southeast2/qoffea-backend/metrics?project=qoffea-backend-7133
```

### 4. Monthly Tasks

```powershell
# 1. Review billing
gcloud billing accounts list
# Check: https://console.cloud.google.com/billing

# 2. Check for updates
gcloud components update

# 3. Review and clean old logs
gcloud logging logs delete projects/qoffea-backend-7133/logs/cloudaudit.googleapis.com%2Factivity

# 4. Review security
gcloud projects get-iam-policy qoffea-backend-7133
```

---

## 🚨 Troubleshooting

### Backend Issues

#### Issue: Backend tidak respond (503 Service Unavailable)

```powershell
# Check service status
gcloud run services describe qoffea-backend --region asia-southeast2

# Check logs untuk error
gcloud run services logs tail qoffea-backend --region asia-southeast2

# Possible solutions:
# 1. Restart service (deploy ulang)
# 2. Check memory limits
# 3. Check if model download failed
```

#### Issue: Request timeout

```powershell
# Increase timeout
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --timeout 600

# Check if instance is cold starting
# Solution: Set min-instances to 1
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --min-instances 1
```

#### Issue: Out of memory

```powershell
# Check memory usage in logs
gcloud run services logs read qoffea-backend \
  --region asia-southeast2 \
  --filter="memory"

# Increase memory
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --memory 8Gi
```

#### Issue: Model loading failed

```powershell
# Check logs
gcloud run services logs tail qoffea-backend --region asia-southeast2

# Verify environment variables
gcloud run services describe qoffea-backend \
  --region asia-southeast2 \
  --format="value(spec.template.spec.containers[0].env)"

# Check if Hugging Face repo accessible
# Test manually: https://huggingface.co/rakaval/coffea
```

### Frontend Issues

#### Issue: 404 Not Found

```powershell
# Check if file exists
gcloud storage ls gs://qoffea-frontend-7133/index.html

# Check if bucket is public
gcloud storage buckets describe gs://qoffea-frontend-7133

# Re-upload file
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea"
gcloud storage cp index.html gs://qoffea-frontend-7133/
```

#### Issue: CORS Error

```powershell
# Set CORS policy
echo '[{"origin": ["*"], "method": ["GET", "POST"], "maxAgeSeconds": 3600}]' > cors.json
gcloud storage buckets update gs://qoffea-frontend-7133 --cors-file=cors.json
```

#### Issue: CSS/JS not loading

```powershell
# Check content-type
gcloud storage objects describe gs://qoffea-frontend-7133/css/app.css

# Update content-type
gcloud storage objects update gs://qoffea-frontend-7133/css/*.css \
  --content-type=text/css

gcloud storage objects update gs://qoffea-frontend-7133/js/*.js \
  --content-type=application/javascript
```

---

## 💰 Cost Monitoring

### Check Current Costs

```powershell
# Via CLI (approximate)
gcloud billing accounts list

# Better: Use Web Console
# https://console.cloud.google.com/billing?project=qoffea-backend-7133
```

### Cost Breakdown

**Typical Monthly Costs (Low Traffic):**
- Cloud Run: $5-15
  - First 2 million requests: FREE
  - $0.40 per million requests after
  - Memory: $0.0000025 per GB-second
  - CPU: $0.00002400 per vCPU-second
  
- Cloud Storage: $0.50-2
  - Storage: $0.020 per GB/month
  - Operations: Mostly free tier
  - Network egress: $0.12 per GB (after 1GB free)

- Cloud Build: FREE (120 build-minutes/day free)

**Total Estimated: $5-20/month** for low-medium traffic

### Set Budget Alerts

1. Buka https://console.cloud.google.com/billing/budgets?project=qoffea-backend-7133
2. Click "Create Budget"
3. Set amount: $50/month
4. Set alerts at: 50%, 90%, 100%

### Cost Optimization Tips

```powershell
# 1. Set max instances to limit scaling
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --max-instances 3

# 2. Use min-instances=0 to scale to zero when idle
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --min-instances 0

# 3. Enable Cloud CDN untuk reduce egress
# (Via Console - Cloud Storage settings)

# 4. Delete unused revisions
gcloud run revisions delete OLD_REVISION --region asia-southeast2
```

---

## 📊 Performance Optimization

### Backend Optimization

```powershell
# 1. Enable CPU throttling (save cost)
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --cpu-throttling

# 2. Set request timeout
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --timeout 120

# 3. Optimize concurrency
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --concurrency 80
```

### Frontend Optimization

```powershell
# 1. Enable compression
gcloud storage objects update gs://qoffea-frontend-7133/** \
  --content-encoding=gzip

# 2. Set long cache for assets
gcloud storage objects update gs://qoffea-frontend-7133/Assets/** \
  --cache-control="public, max-age=31536000"

# 3. Set short cache for HTML
gcloud storage objects update gs://qoffea-frontend-7133/*.html \
  --cache-control="public, max-age=300"
```

---

## 🔐 Security Best Practices

### 1. IAM & Permissions

```powershell
# List current IAM policies
gcloud projects get-iam-policy qoffea-backend-7133

# Remove unnecessary members
gcloud projects remove-iam-policy-binding qoffea-backend-7133 \
  --member="user:example@gmail.com" \
  --role="roles/editor"
```

### 2. Enable Audit Logging

```powershell
# View audit logs
gcloud logging read "resource.type=cloud_run_revision" \
  --project=qoffea-backend-7133 \
  --limit=50
```

### 3. Secret Management

```powershell
# Don't put secrets in env vars!
# Use Secret Manager instead:

# Create secret
echo -n "my-secret-key" | gcloud secrets create flask-secret-key --data-file=-

# Use in Cloud Run
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --update-secrets=SECRET_KEY=flask-secret-key:latest
```

---

## 📝 Maintenance Schedule

### Daily (Automated)
- ✅ Health check monitoring
- ✅ Error log monitoring
- ✅ Auto-scaling based on traffic

### Weekly (Manual - 15 mins)
```powershell
# 1. Check metrics
# Open: https://console.cloud.google.com/run/detail/asia-southeast2/qoffea-backend/metrics

# 2. Review error logs
gcloud run services logs read qoffea-backend \
  --region asia-southeast2 \
  --filter="severity>=ERROR" \
  --limit=50

# 3. Check costs
# Open: https://console.cloud.google.com/billing
```

### Monthly (Manual - 30 mins)
```powershell
# 1. Update dependencies
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Backend-Qoffea"
# Update requirements.txt jika ada security updates

# 2. Review and optimize costs
# 3. Clean up old revisions
gcloud run revisions list --service qoffea-backend --region asia-southeast2
# Delete old ones

# 4. Update documentation
```

---

## 🆘 Emergency Procedures

### Service Down - Emergency Response

```powershell
# 1. Check service status IMMEDIATELY
gcloud run services describe qoffea-backend --region asia-southeast2

# 2. Check logs for critical errors
gcloud run services logs tail qoffea-backend \
  --region asia-southeast2 \
  --filter="severity>=ERROR"

# 3. Quick fix: Redeploy last working revision
gcloud run revisions list --service qoffea-backend --region asia-southeast2
gcloud run services update-traffic qoffea-backend \
  --region asia-southeast2 \
  --to-revisions LAST_WORKING_REVISION=100

# 4. If still down: Delete and redeploy
gcloud run services delete qoffea-backend --region asia-southeast2
# Then deploy again
```

### Budget Exceeded

```powershell
# 1. Stop service immediately
gcloud run services delete qoffea-backend --region asia-southeast2

# 2. Check what caused spike
# Open: https://console.cloud.google.com/billing

# 3. Set stricter limits before redeploying
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --max-instances 2 \
  --memory 2Gi
```

---

## 📚 Additional Resources

### Documentation
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Cloud Monitoring](https://cloud.google.com/monitoring/docs)

### Support
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow - google-cloud-run](https://stackoverflow.com/questions/tagged/google-cloud-run)

### Tools
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [Cloud Console](https://console.cloud.google.com)

---

**Last Updated:** November 3, 2025
**Maintained by:** Qoffea Team
**Project:** qoffea-backend-7133
