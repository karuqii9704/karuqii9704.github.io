# Script to check SSL Certificate provisioning status
# Run this script periodically to check if SSL is ready

Write-Host "`n🔒 Checking SSL Certificate Status...`n" -ForegroundColor Cyan

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Get SSL certificate status
$status = gcloud compute ssl-certificates describe qoffea-ssl-cert --global --project=qoffea-backend-7133 --format="value(managed.status)"

Write-Host "Certificate Status: " -NoNewline
if ($status -eq "ACTIVE") {
    Write-Host "$status" -ForegroundColor Green
    Write-Host "`n✅ SSL Certificate is ACTIVE!`n" -ForegroundColor Green
    Write-Host "Your website is now available at:" -ForegroundColor Green
    Write-Host "  🌐 https://34-49-190-69.nip.io/index.html"
    Write-Host "  🌐 https://34-49-190-69.nip.io/aksi.html"
    Write-Host "  🌐 https://34-49-190-69.nip.io/panduan.html"
    Write-Host "`nTesting HTTPS connection..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "https://34-49-190-69.nip.io/index.html" -UseBasicParsing -TimeoutSec 10
        Write-Host "✅ HTTPS is working! Status Code: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  HTTPS test failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} elseif ($status -eq "PROVISIONING") {
    Write-Host "$status" -ForegroundColor Yellow
    Write-Host "`n⏳ SSL Certificate is still being provisioned..." -ForegroundColor Yellow
    Write-Host "This typically takes 15-60 minutes.`n"
    
    # Get domain status
    Write-Host "Domain Status:" -ForegroundColor Cyan
    gcloud compute ssl-certificates describe qoffea-ssl-cert --global --project=qoffea-backend-7133 --format="yaml(managed.domainStatus)"
    
    Write-Host "`n💡 Tips while waiting:" -ForegroundColor Cyan
    Write-Host "  1. DNS propagation might take time"
    Write-Host "  2. Google needs to verify domain ownership"
    Write-Host "  3. Run this script again in 10-15 minutes"
    Write-Host "`nRun this script again with: .\check-ssl-status.ps1"
} else {
    Write-Host "$status" -ForegroundColor Red
    Write-Host "`n❌ SSL Certificate has failed!`n" -ForegroundColor Red
    Write-Host "Full certificate details:"
    gcloud compute ssl-certificates describe qoffea-ssl-cert --global --project=qoffea-backend-7133
}

Write-Host ""
