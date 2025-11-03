# 🌐 Custom Domain Setup Guide - Qoffea

Panduan lengkap untuk setup custom domain untuk aplikasi Qoffea di Google Cloud Platform.

## 📋 Overview

Dengan custom domain, aplikasi Anda bisa diakses dengan nama yang lebih profesional:

**Sebelum (default):**

- Backend: `https://qoffea-backend-c26brvbilq-et.a.run.app`
- Frontend: `https://storage.googleapis.com/qoffea-frontend-7133/index.html`

**Sesudah (custom domain):**

- Backend: `https://api.qoffea.com` atau `https://qoffea.com/api`
- Frontend: `https://qoffea.com` atau `https://www.qoffea.com`

---

## 🎯 Opsi Custom Domain

### Opsi 1: Gunakan Domain yang Sudah Ada

Jika Anda sudah punya domain (misal dari Namecheap, GoDaddy, dll)

### Opsi 2: Beli Domain Baru

Beli dari:

- **Google Domains** (recommended) - $12-20/tahun
- **Namecheap** - $8-15/tahun
- **GoDaddy** - $10-20/tahun
- **Cloudflare** - $9-15/tahun

### Opsi 3: Domain Gratis (untuk testing)

- **Freenom** (.tk, .ml, .ga, .cf, .gq) - GRATIS
- **InfinityFree** dengan domain gratis
- **EU.org** subdomain - GRATIS

---

## 🚀 Setup Custom Domain untuk Backend (Cloud Run)

### Prerequisites

- Domain sudah dibeli/dimiliki
- Akses ke DNS management domain

### Step 1: Verify Domain Ownership di Google Cloud

```powershell
# 1. Buka Google Search Console untuk verify
# https://search.google.com/search-console

# 2. Atau verify via gcloud
gcloud domains verify DOMAIN_NAME
```

### Step 2: Map Domain ke Cloud Run

**Via Web Console (RECOMMENDED):**

1. Buka Cloud Run Console:

   ```
   https://console.cloud.google.com/run/detail/asia-southeast2/qoffea-backend/networking?project=qoffea-backend-7133
   ```

2. Klik tab **"Domain Mappings"**

3. Klik **"Add Mapping"**

4. Pilih service: `qoffea-backend`

5. Masukkan domain Anda, misal:

   - `api.qoffea.com` (untuk backend API)
   - atau `qoffea.com` (root domain)

6. Klik **"Continue"**

7. Google akan memberikan DNS records yang perlu ditambahkan

**Via CLI:**

```powershell
# Map domain ke Cloud Run service
gcloud run domain-mappings create \
  --service qoffea-backend \
  --domain api.qoffea.com \
  --region asia-southeast2 \
  --project qoffea-backend-7133
```

### Step 3: Update DNS Records

Setelah mapping, Google akan memberikan DNS records. Tambahkan ke DNS provider Anda:

**Jika menggunakan subdomain (api.qoffea.com):**

```
Type: CNAME
Name: api
Value: ghs.googlehosted.com
TTL: 3600 (1 hour)
```

**Jika menggunakan root domain (qoffea.com):**

```
Type: A
Name: @
Value: 216.239.32.21
TTL: 3600

Type: A
Name: @
Value: 216.239.34.21
TTL: 3600

Type: A
Name: @
Value: 216.239.36.21
TTL: 3600

Type: A
Name: @
Value: 216.239.38.21
TTL: 3600

Type: AAAA
Name: @
Value: 2001:4860:4802:32::15
TTL: 3600

Type: AAAA
Name: @
Value: 2001:4860:4802:34::15
TTL: 3600

Type: AAAA
Name: @
Value: 2001:4860:4802:36::15
TTL: 3600

Type: AAAA
Name: @
Value: 2001:4860:4802:38::15
TTL: 3600
```

### Step 4: Wait for DNS Propagation

```powershell
# Check DNS propagation (tunggu 5-60 menit)
nslookup api.qoffea.com

# Or use online tool:
# https://dnschecker.org
```

### Step 5: Verify Custom Domain

```powershell
# Test dengan curl
Invoke-RestMethod -Uri "https://api.qoffea.com/api/health"

# Expected: Status 200 OK dengan response JSON
```

### Step 6: Update Frontend API URL

```powershell
# Update app.js dengan custom domain
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea\js"
```

Edit `app.js`:

```javascript
// Ganti dari:
const API_BASE_URL = "https://qoffea-backend-c26brvbilq-et.a.run.app/api";

// Menjadi:
const API_BASE_URL = "https://api.qoffea.com/api";
```

Deploy ulang frontend:

```powershell
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea"
gcloud storage cp -r . gs://qoffea-frontend-7133/
```

---

## 🎨 Setup Custom Domain untuk Frontend (Cloud Storage)

### Opsi A: Menggunakan Load Balancer (RECOMMENDED)

Load Balancer memberikan:

- ✅ Custom domain dengan HTTPS
- ✅ SSL certificate otomatis
- ✅ CDN built-in untuk performance
- ✅ HTTP to HTTPS redirect

**Step 1: Reserve Static IP**

```powershell
# Reserve global static IP
gcloud compute addresses create qoffea-frontend-ip \
  --global \
  --project qoffea-backend-7133

# Get the IP address
gcloud compute addresses describe qoffea-frontend-ip \
  --global \
  --format="value(address)"
```

**Step 2: Create Load Balancer via Web Console**

1. Buka Load Balancer Console:

   ```
   https://console.cloud.google.com/net-services/loadbalancing?project=qoffea-backend-7133
   ```

2. Klik **"Create Load Balancer"**

3. Pilih **"HTTP(S) Load Balancing"**

4. Pilih **"From Internet to my VMs or serverless services"**

5. Klik **"Continue"**

6. **Backend Configuration:**

   - Backend type: **Backend buckets**
   - Klik **"Create backend bucket"**
   - Name: `qoffea-frontend-backend`
   - Cloud Storage bucket: `qoffea-frontend-7133`
   - Enable Cloud CDN: ✅ (untuk performance)

7. **Host and path rules:**

   - Default (no specific rules needed)

8. **Frontend Configuration:**

   - Protocol: **HTTPS**
   - IP: Select `qoffea-frontend-ip`
   - Certificate: **Create Google-managed certificate**

     - Domains: `qoffea.com, www.qoffea.com`

   - Add another frontend for HTTP redirect:
     - Protocol: **HTTP**
     - IP: Same `qoffea-frontend-ip`
     - Redirect to HTTPS: ✅

9. Klik **"Create"**

**Step 3: Update DNS Records**

Arahkan domain Anda ke IP Load Balancer:

```
Type: A
Name: @
Value: [IP dari step 1]
TTL: 3600

Type: A
Name: www
Value: [IP dari step 1]
TTL: 3600
```

**Step 4: Wait for SSL Certificate**

```powershell
# Check certificate status (bisa memakan waktu 15-60 menit)
gcloud compute ssl-certificates list --project qoffea-backend-7133

# Status harus ACTIVE
```

**Step 5: Test Custom Domain**

```powershell
# Test akses
Start-Process "https://qoffea.com"
Start-Process "https://www.qoffea.com"

# Check SSL
Invoke-WebRequest -Uri "https://qoffea.com" | Select-Object -ExpandProperty StatusCode
# Expected: 200
```

### Opsi B: Menggunakan Firebase Hosting (ALTERNATIVE)

Firebase Hosting lebih mudah dan include SSL gratis:

**Step 1: Install Firebase CLI**

```powershell
npm install -g firebase-tools
```

**Step 2: Initialize Firebase**

```powershell
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea"

# Login
firebase login

# Initialize
firebase init hosting
```

Jawab pertanyaan:

- **Project:** Create new atau pilih existing
- **Public directory:** `.` (current directory)
- **Single page app:** No
- **Overwrite files:** No

**Step 3: Deploy**

```powershell
firebase deploy --only hosting
```

**Step 4: Add Custom Domain**

```powershell
# Via CLI
firebase hosting:channel:deploy live --only qoffea.com

# Or via Firebase Console:
# https://console.firebase.google.com
# Go to Hosting > Add custom domain
```

Firebase akan otomatis setup SSL certificate!

---

## 🔧 Complete Setup Example

### Contoh dengan domain: `qoffea.com`

**Target URLs:**

- Frontend: `https://qoffea.com`
- Backend API: `https://api.qoffea.com`

**Step-by-Step:**

1. **Beli domain** `qoffea.com` (misal dari Namecheap)

2. **Setup Backend API subdomain:**

   ```powershell
   # Map Cloud Run
   gcloud run domain-mappings create \
     --service qoffea-backend \
     --domain api.qoffea.com \
     --region asia-southeast2
   ```

3. **Add DNS Record untuk API:**

   - Di Namecheap DNS settings:

   ```
   Type: CNAME
   Host: api
   Value: ghs.googlehosted.com
   ```

4. **Setup Frontend dengan Load Balancer:**

   ```powershell
   # Reserve IP
   gcloud compute addresses create qoffea-frontend-ip --global

   # Get IP
   $IP = gcloud compute addresses describe qoffea-frontend-ip --global --format="value(address)"
   Write-Host "IP Address: $IP"
   ```

5. **Add DNS Records untuk Frontend:**

   ```
   Type: A
   Host: @
   Value: [IP dari step 4]

   Type: A
   Host: www
   Value: [IP dari step 4]
   ```

6. **Create Load Balancer via Console** (seperti langkah di atas)

7. **Update Frontend API URL:**

   ```javascript
   // Frontend-Qoffea/js/app.js
   const API_BASE_URL = "https://api.qoffea.com/api";
   ```

8. **Deploy Frontend:**

   ```powershell
   cd Frontend-Qoffea
   gcloud storage cp -r . gs://qoffea-frontend-7133/
   ```

9. **Wait & Test** (15-60 menit untuk DNS & SSL):

   ```powershell
   # Test Frontend
   Start-Process "https://qoffea.com"

   # Test Backend
   Invoke-RestMethod -Uri "https://api.qoffea.com/api/health"
   ```

---

## 💰 Cost Estimation

### Domain Cost (Annual)

- **.com domain:** $12-15/tahun
- **.id domain:** $15-20/tahun
- **Free domain (.tk, .ml, dll):** $0

### Google Cloud Cost (Monthly)

- **Cloud Run (Backend):** $5-20/bulan (unchanged)
- **Cloud Storage (Frontend):** $0.50-2/bulan (unchanged)
- **Load Balancer:**
  - Forwarding rules: $0.025/hour = ~$18/bulan
  - Data processed: $0.008-0.02/GB
  - **Total:** ~$20-30/bulan
- **SSL Certificate:** FREE (Google-managed)

### Alternative: Firebase Hosting

- **FREE tier:** 10GB storage + 360MB/day bandwidth
- **Paid (Blaze):** $0.026/GB storage + $0.15/GB bandwidth
- **SSL Certificate:** FREE
- **Custom domain:** FREE
- **Total:** $0-5/bulan (much cheaper!)

**RECOMMENDATION:** Gunakan **Firebase Hosting** untuk Frontend jika budget terbatas!

---

## 🎯 Recommended Setup (Budget-Friendly)

### Setup Optimal:

1. **Frontend:** Firebase Hosting (FREE atau ~$2/bulan)

   - Custom domain: `qoffea.com`
   - SSL gratis
   - CDN built-in

2. **Backend:** Cloud Run (unchanged)
   - Custom domain: `api.qoffea.com`
   - Cost: $5-20/bulan

**Total: ~$10-25/bulan + $12/tahun domain**

---

## 📝 DNS Configuration Checklist

### For Backend API (api.qoffea.com)

```
✅ CNAME record: api -> ghs.googlehosted.com
✅ Wait 5-60 minutes for propagation
✅ Verify with: nslookup api.qoffea.com
✅ Test with: curl https://api.qoffea.com/api/health
```

### For Frontend (qoffea.com)

**Option 1: Load Balancer**

```
✅ A record: @ -> [Load Balancer IP]
✅ A record: www -> [Load Balancer IP]
✅ Wait 15-60 minutes for SSL provisioning
✅ Verify with: nslookup qoffea.com
✅ Test with: curl https://qoffea.com
```

**Option 2: Firebase Hosting**

```
✅ A record: @ -> [Firebase IPs from console]
✅ CNAME record: www -> [Firebase domain]
✅ Wait 24-48 hours for SSL provisioning
✅ Verify in Firebase Console
✅ Test with: curl https://qoffea.com
```

---

## 🔍 Troubleshooting

### Issue: DNS tidak resolve

```powershell
# Check DNS propagation
nslookup qoffea.com
nslookup api.qoffea.com

# Use online checker
# https://dnschecker.org
# https://www.whatsmydns.net

# Common issues:
# 1. Tunggu 5-60 menit untuk propagasi
# 2. Clear DNS cache
ipconfig /flushdns

# 3. Check di multiple DNS servers
nslookup qoffea.com 8.8.8.8  # Google DNS
nslookup qoffea.com 1.1.1.1  # Cloudflare DNS
```

### Issue: SSL Certificate Pending

```powershell
# Check certificate status
gcloud compute ssl-certificates list

# Possible reasons:
# 1. DNS belum propagate (tunggu 15-60 menit)
# 2. Domain verification gagal
# 3. CAA record blocking (check di DNS provider)

# Solution: Wait atau check Google Cloud Console logs
```

### Issue: Cloud Run mapping failed

```powershell
# Check domain mapping status
gcloud run domain-mappings describe api.qoffea.com \
  --service qoffea-backend \
  --region asia-southeast2

# Delete and recreate if needed
gcloud run domain-mappings delete api.qoffea.com \
  --service qoffea-backend \
  --region asia-southeast2

gcloud run domain-mappings create \
  --service qoffea-backend \
  --domain api.qoffea.com \
  --region asia-southeast2
```

### Issue: CORS error dengan custom domain

Update Backend CORS settings:

```powershell
# Update environment variable
gcloud run services update qoffea-backend \
  --region asia-southeast2 \
  --set-env-vars "CORS_ORIGINS=https://qoffea.com,https://www.qoffea.com"
```

Or edit `Backend-Qoffea/config.py`:

```python
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://qoffea.com,https://www.qoffea.com,*')
```

---

## 🚀 Quick Start Commands

### Setup Backend Custom Domain

```powershell
# 1. Map domain
gcloud run domain-mappings create \
  --service qoffea-backend \
  --domain api.yourdomain.com \
  --region asia-southeast2

# 2. Get DNS records to add
echo "Add CNAME record:"
echo "Host: api"
echo "Value: ghs.googlehosted.com"

# 3. Wait and test
Start-Sleep -Seconds 300  # Wait 5 minutes
Invoke-RestMethod -Uri "https://api.yourdomain.com/api/health"
```

### Setup Frontend with Firebase (Recommended)

```powershell
# 1. Install Firebase CLI
npm install -g firebase-tools

# 2. Initialize
cd "e:\ACOOLLYEAHHH\New folder\karuqii9704.github.io\Frontend-Qoffea"
firebase login
firebase init hosting

# 3. Deploy
firebase deploy --only hosting

# 4. Add custom domain in Firebase Console
# https://console.firebase.google.com -> Hosting -> Add custom domain
```

---

## 📚 Additional Resources

- [Cloud Run Custom Domains](https://cloud.google.com/run/docs/mapping-custom-domains)
- [Cloud Load Balancer Setup](https://cloud.google.com/load-balancing/docs/https)
- [Firebase Custom Domains](https://firebase.google.com/docs/hosting/custom-domain)
- [Google Domain Verification](https://support.google.com/webmasters/answer/9008080)
- [DNS Propagation Checker](https://dnschecker.org)

---

## ✅ Summary

**Untuk setup custom domain:**

1. **Beli domain** (atau gunakan yang sudah ada)
2. **Backend:** Map domain via Cloud Run (subdomain recommended: api.yourdomain.com)
3. **Frontend:** Deploy via Firebase Hosting (paling mudah & murah) ATAU Load Balancer (lebih powerful)
4. **Update DNS records** di domain provider
5. **Update API URL** di frontend code
6. **Wait for propagation** (15-60 menit)
7. **Test & Monitor**

**Recommended Setup:**

- Domain: Beli di Namecheap/GoDaddy (~$12/tahun)
- Backend: Cloud Run dengan subdomain `api.yourdomain.com`
- Frontend: Firebase Hosting dengan root domain `yourdomain.com`
- Total: ~$10-25/bulan + $12/tahun

---

**Need Help?** Contact Google Cloud Support atau check documentation di link di atas!

**Last Updated:** November 3, 2025
