/**
 * Qoffea Frontend - Main Application Script
 * Handles image upload, analysis, and result display
 */

// API Configuration
const API_BASE_URL = 'https://qoffea-backend-c26brvbilq-et.a.run.app/api';

// Global state
let currentAnalysisId = null;
let uploadedImage = null;
let cameraStream = null;
let videoElement = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    hideResultsSection();
    createCameraModal();
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // Camera button
    const cameraBtn = document.getElementById('openCameraBtn');
    if (cameraBtn) {
        cameraBtn.addEventListener('click', openCamera);
    }
    
    // Gallery button
    const galleryBtn = document.getElementById('openGalleryBtn');
    if (galleryBtn) {
        galleryBtn.addEventListener('click', openGallery);
    }
    
    // File input
    const fileInput = document.getElementById('imageInput');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    // Download PDF button
    const downloadBtn = document.getElementById('downloadPdfBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadPDF);
    }
    
    // Analyze again button
    const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');
    if (analyzeAgainBtn) {
        analyzeAgainBtn.addEventListener('click', resetAnalysis);
    }
}

/**
 * Create camera modal
 */
function createCameraModal() {
    const modalHtml = `
        <div class="modal fade" id="cameraModal" tabindex="-1" aria-labelledby="cameraModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="cameraModalLabel">Ambil Foto Biji Kopi</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                        <video id="cameraVideo" autoplay playsinline style="width: 100%; max-width: 640px; border-radius: 8px; background: #000;"></video>
                        <canvas id="cameraCanvas" style="display: none;"></canvas>
                        <div id="cameraError" class="alert alert-danger mt-3" style="display: none;"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                        <button type="button" class="btn btn-qoffea-primary" id="capturePhotoBtn">
                            <i class="bi bi-camera-fill"></i> Ambil Foto
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Setup capture button
    const captureBtn = document.getElementById('capturePhotoBtn');
    if (captureBtn) {
        captureBtn.addEventListener('click', capturePhoto);
    }
    
    // Setup modal events
    const cameraModal = document.getElementById('cameraModal');
    if (cameraModal) {
        cameraModal.addEventListener('shown.bs.modal', startCamera);
        cameraModal.addEventListener('hidden.bs.modal', stopCamera);
    }
}

/**
 * Open camera for capturing image
 */
async function openCamera() {
    const cameraModal = new bootstrap.Modal(document.getElementById('cameraModal'));
    cameraModal.show();
}

/**
 * Start camera stream
 */
async function startCamera() {
    videoElement = document.getElementById('cameraVideo');
    const errorDiv = document.getElementById('cameraError');
    
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showCameraError('Browser Anda tidak mendukung akses kamera');
        return;
    }
    
    try {
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment', // Prefer rear camera on mobile
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        });
        
        videoElement.srcObject = cameraStream;
        errorDiv.style.display = 'none';
        
    } catch (error) {
        console.error('Camera error:', error);
        let errorMessage = 'Gagal mengakses kamera. ';
        
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
            errorMessage += 'Izin kamera ditolak. Silakan izinkan akses kamera di pengaturan browser.';
        } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
            errorMessage += 'Kamera tidak ditemukan pada perangkat ini.';
        } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
            errorMessage += 'Kamera sedang digunakan oleh aplikasi lain.';
        } else {
            errorMessage += error.message;
        }
        
        showCameraError(errorMessage);
    }
}

/**
 * Stop camera stream
 */
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    if (videoElement) {
        videoElement.srcObject = null;
    }
}

/**
 * Capture photo from camera
 */
function capturePhoto() {
    if (!videoElement || !cameraStream) {
        showError('Kamera belum siap');
        return;
    }
    
    const canvas = document.getElementById('cameraCanvas');
    const context = canvas.getContext('2d');
    
    // Set canvas dimensions to match video
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    
    // Draw current video frame to canvas
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to blob
    canvas.toBlob(function(blob) {
        if (!blob) {
            showError('Gagal mengambil foto');
            return;
        }
        
        // Create file from blob
        const file = new File([blob], 'camera_capture.jpg', { type: 'image/jpeg' });
        
        // Close modal
        const cameraModal = bootstrap.Modal.getInstance(document.getElementById('cameraModal'));
        if (cameraModal) {
            cameraModal.hide();
        }
        
        // Display preview and analyze
        uploadedImage = file;
        displayPreview(file);
        uploadAndAnalyze(file);
        
    }, 'image/jpeg', 0.9);
}

/**
 * Show camera error message
 */
function showCameraError(message) {
    const errorDiv = document.getElementById('cameraError');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
    
    const videoElement = document.getElementById('cameraVideo');
    if (videoElement) {
        videoElement.style.display = 'none';
    }
    
    const captureBtn = document.getElementById('capturePhotoBtn');
    if (captureBtn) {
        captureBtn.disabled = true;
    }
}

/**
 * Open gallery for selecting image
 */
function openGallery() {
    const fileInput = document.getElementById('imageInput');
    if (fileInput) {
        fileInput.click();
    } else {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/jpeg,image/png,image/jpg';
        input.addEventListener('change', handleFileSelect);
        input.click();
    }
}

/**
 * Handle file selection
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) {
        return;
    }
    
    // Validate file type
    if (!file.type.match('image/(jpeg|jpg|png)')) {
        showError('Format file tidak valid. Gunakan JPG, JPEG, atau PNG.');
        return;
    }
    
    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
        showError('Ukuran file terlalu besar. Maksimal 10MB.');
        return;
    }
    
    uploadedImage = file;
    
    // Display preview
    displayPreview(file);
    
    // Upload and analyze
    uploadAndAnalyze(file);
}

/**
 * Display image preview
 */
function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewImg = document.querySelector('.upload-section__preview-image');
        if (previewImg) {
            previewImg.src = e.target.result;
        }
    };
    reader.readAsDataURL(file);
}

/**
 * Upload image and analyze
 */
async function uploadAndAnalyze(file) {
    showLoading('Menganalisis gambar...');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('source', 'gallery');
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentAnalysisId = result.analysis_id;
            displayResults(result);
            hideLoading();
        } else {
            throw new Error(result.error || 'Analisis gagal');
        }
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showError('Gagal menganalisis gambar: ' + error.message);
    }
}

/**
 * Display analysis results
 */
function displayResults(result) {
    const analysis = result.analysis;
    
    // Update percentages
    updatePercentageDisplay(analysis);
    
    // Update statistics
    updateStatistics(analysis);
    
    // Display annotated image if available
    if (result.annotated_filename) {
        displayAnnotatedImage(result.annotated_filename);
    }
    
    // Show results section
    showResultsSection();
}

/**
 * Update percentage display
 */
function updatePercentageDisplay(analysis) {
    const goodPercentage = analysis.good_percentage;
    const defectPercentage = analysis.defect_percentage;
    
    // Update text percentages
    document.querySelectorAll('.grade-text__item').forEach(item => {
        if (item.classList.contains('grade-text--good')) {
            item.querySelector('span').textContent = goodPercentage.toFixed(1) + '%';
        } else if (item.classList.contains('grade-text--defect')) {
            item.querySelector('span').textContent = defectPercentage.toFixed(1) + '%';
        }
    });
    
    // Update visual bar
    const goodBar = document.querySelector('.segment-good');
    const defectBar = document.querySelector('.segment-defect');
    
    if (goodBar) {
        goodBar.style.height = goodPercentage + '%';
        goodBar.setAttribute('title', `Good: ${goodPercentage.toFixed(1)}%`);
    }
    
    if (defectBar) {
        defectBar.style.height = defectPercentage + '%';
        defectBar.setAttribute('title', `Defect: ${defectPercentage.toFixed(1)}%`);
    }
}

/**
 * Update statistics display
 */
function updateStatistics(analysis) {
    const statsHtml = `
        <div class="statistics-grid">
            <div class="stat-item">
                <span class="stat-label">Total Biji:</span>
                <span class="stat-value">${analysis.total_beans}</span>
            </div>
            <div class="stat-item stat-good">
                <span class="stat-label">Biji Baik:</span>
                <span class="stat-value">${analysis.good_beans}</span>
            </div>
            <div class="stat-item stat-defect">
                <span class="stat-label">Biji Cacat:</span>
                <span class="stat-value">${analysis.defect_beans}</span>
            </div>
        </div>
    `;
    
    // Find or create statistics container
    let statsContainer = document.querySelector('.statistics-container');
    if (!statsContainer) {
        statsContainer = document.createElement('div');
        statsContainer.className = 'statistics-container mt-3';
        const resultsBody = document.querySelector('.results-section__body');
        if (resultsBody) {
            resultsBody.insertBefore(statsContainer, resultsBody.firstChild);
        }
    }
    statsContainer.innerHTML = statsHtml;
}

/**
 * Display annotated image
 */
function displayAnnotatedImage(filename) {
    // Use backend API URL for annotated image
    const imageUrl = `${API_BASE_URL.replace('/api', '')}/uploads/${filename}`;
    
    const analysisImage = document.querySelector('.analysis-image-section img');
    if (analysisImage) {
        analysisImage.src = imageUrl;
        analysisImage.alt = 'Analisis Biji Kopi dengan Deteksi';
        console.log('Loading annotated image from:', imageUrl);
        
        // Add error handler for image loading
        analysisImage.onerror = function() {
            console.error('Failed to load image from:', imageUrl);
            showError('Gambar hasil analisis gagal dimuat. File mungkin sudah dihapus dari server (ephemeral storage).');
        };
        
        // Add success handler
        analysisImage.onload = function() {
            console.log('Image loaded successfully from:', imageUrl);
        };
    }
}

/**
 * Download PDF report
 */
async function downloadPDF() {
    if (!currentAnalysisId) {
        showError('Tidak ada analisis untuk diunduh');
        return;
    }
    
    showLoading('Membuat PDF...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/report/${currentAnalysisId}/download`);
        
        if (!response.ok) {
            throw new Error('Gagal membuat PDF');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `qoffea_report_${currentAnalysisId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        hideLoading();
        showSuccess('PDF berhasil diunduh!');
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showError('Gagal mengunduh PDF: ' + error.message);
    }
}

/**
 * Reset analysis for new upload
 */
function resetAnalysis() {
    currentAnalysisId = null;
    uploadedImage = null;
    hideResultsSection();
    
    // Reset preview image
    const previewImg = document.querySelector('.upload-section__preview-image');
    if (previewImg) {
        previewImg.src = 'Assets/coffe_beans.jpg';
    }
}

/**
 * Show loading indicator
 */
function showLoading(message = 'Loading...') {
    let loader = document.getElementById('loadingOverlay');
    
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loadingOverlay';
        loader.className = 'loading-overlay';
        loader.innerHTML = `
            <div class="loading-content">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="loading-text mt-3">${message}</p>
            </div>
        `;
        document.body.appendChild(loader);
    } else {
        loader.querySelector('.loading-text').textContent = message;
        loader.style.display = 'flex';
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loader = document.getElementById('loadingOverlay');
    if (loader) {
        loader.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    alert('Error: ' + message);
    // TODO: Implement better error UI
}

/**
 * Show success message
 */
function showSuccess(message) {
    alert(message);
    // TODO: Implement better success UI
}

/**
 * Show results section
 */
function showResultsSection() {
    const resultsSection = document.querySelector('.results-section');
    const analysisSection = document.querySelector('.analysis-image-section');
    const samplesSection = document.querySelector('.samples-section');
    const analyzeAgainSection = document.querySelector('.text-center.mb-4:last-child');
    
    if (resultsSection) resultsSection.style.display = 'block';
    if (analysisSection) analysisSection.style.display = 'block';
    if (samplesSection) samplesSection.style.display = 'none'; // Hide samples for now
    if (analyzeAgainSection) analyzeAgainSection.style.display = 'block';
}

/**
 * Hide results section
 */
function hideResultsSection() {
    const resultsSection = document.querySelector('.results-section');
    const analysisSection = document.querySelector('.analysis-image-section');
    const analyzeAgainSection = document.querySelector('.text-center.mb-4:last-child');
    
    if (resultsSection) resultsSection.style.display = 'none';
    if (analysisSection) analysisSection.style.display = 'none';
    if (analyzeAgainSection) analyzeAgainSection.style.display = 'none';
}
