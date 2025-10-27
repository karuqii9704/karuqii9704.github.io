// 1. Ambil elemen-elemen yang kita butuhkan
const fileInput = document.getElementById('fileUploadInput');
const dropZone = document.querySelector('.drag-drop-zone');
const dropZoneText = dropZone.querySelector('.fw-bold'); // Teks "Tekan atau tarik..."
const originalDropZoneText = dropZoneText.textContent; // Simpan teks aslinya

// 2. Logika saat file dipilih (via klik)
fileInput.addEventListener('change', (e) => {
    // Cek apakah ada file yang dipilih
    if (e.target.files.length > 0) {
        const fileName = e.target.files[0].name;
        dropZoneText.textContent = `✅ File terpilih: ${fileName}`; // Ubah teksnya
        dropZone.classList.add('file-selected'); // Tambah class untuk styling (opsional)
    }
});

// 3. Logika untuk Drag & Drop

// Saat file diseret ke atas drop zone
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault(); // Wajib biar 'drop' bisa berfungsi
    dropZone.classList.add('drag-over');
});

// Saat file meninggalkan drop zone
dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

// Saat file dilepas (di-drop)
dropZone.addEventListener('drop', (e) => {
    e.preventDefault(); // Wajib biar browser tidak membuka filenya
    dropZone.classList.remove('drag-over');

    // Ambil file yang di-drop
    if (e.dataTransfer.files.length > 0) {
        // Masukkan file yg di-drop ke input file kita
        fileInput.files = e.dataTransfer.files; 
        
        // Tampilkan nama file
        const fileName = e.dataTransfer.files[0].name;
        dropZoneText.textContent = `✅ File terpilih: ${fileName}`;
        dropZone.classList.add('file-selected');
    }
});

// 4. (Opsional) Reset teks saat modal ditutup
const uploadModal = document.getElementById('uploadModal');
uploadModal.addEventListener('hidden.bs.modal', () => {
    dropZoneText.textContent = originalDropZoneText; // Kembalikan teks asli
    dropZone.classList.remove('file-selected'); // Hapus class
    fileInput.value = null; // Kosongkan input file
});