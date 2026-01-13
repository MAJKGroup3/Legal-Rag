
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const uploadBtn = document.getElementById('uploadBtn');
const queryInput = document.getElementById('queryInput');
const queryBtn = document.getElementById('queryBtn');
const resultsContainer = document.getElementById('resultsContainer');
const loading = document.getElementById('loading');
const uploadSuccess = document.getElementById('uploadSuccess');
const uploadError = document.getElementById('uploadError');

let selectedFile = null;

// Upload area click
uploadArea.addEventListener('click', () => fileInput.click());

// File selection
fileInput.addEventListener('change', (e) => {
    selectedFile = e.target.files[0];
    if (selectedFile) {
        fileInfo.textContent = `Selected: ${selectedFile.name} (${(selectedFile.size / 1024 / 1024).toFixed(2)} MB)`;
        uploadBtn.disabled = false;
    }
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    selectedFile = e.dataTransfer.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
        fileInfo.textContent = `Selected: ${selectedFile.name} (${(selectedFile.size / 1024 / 1024).toFixed(2)} MB)`;
        uploadBtn.disabled = false;
    } else {
        fileInfo.textContent = 'Please select a PDF file';
    }
});

// Upload document
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    uploadBtn.disabled = true;
    uploadSuccess.classList.remove('active');
    uploadError.classList.remove('active');
    loading.classList.add('active');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            uploadSuccess.textContent = `✓ ${data.message} (${data.chunk_count} chunks created)`;
            uploadSuccess.classList.add('active');
            fileInfo.textContent = '';
            selectedFile = null;
            fileInput.value = '';
        } else {
            uploadError.textContent = `✗ Error: ${data.detail}`;
            uploadError.classList.add('active');
        }
    } catch (error) {
        uploadError.textContent = `✗ Error: ${error.message}`;
        uploadError.classList.add('active');
    } finally {
        loading.classList.remove('active');
        uploadBtn.disabled = false;
    }
});

// Query documents
queryBtn.addEventListener('click', async () => {
    const query = queryInput.value.trim();
    if (!query) return;

    queryBtn.disabled = true;
    loading.classList.add('active');
    resultsContainer.innerHTML = '';

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, top_k: 5 })
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            resultsContainer.innerHTML = `<div class="error-message active">Error: ${data.detail}</div>`;
        }
    } catch (error) {
        resultsContainer.innerHTML = `<div class="error-message active">Error: ${error.message}</div>`;
    } finally {
        loading.classList.remove('active');
        queryBtn.disabled = false;
    }
});

function displayResults(data) {
    let html = `
                <div class="result-answer">
                    <h3 style="color: #667eea; margin-bottom: 15px;">💡 Answer</h3>
                    <p style="white-space: pre-wrap; line-height: 1.8;">${data.answer}</p>
                </div>
                <h3 style="margin-bottom: 15px; color: #667eea;">📑 Retrieved Chunks (${data.num_chunks})</h3>
                `;

    data.retrieved_chunks.forEach((chunk, idx) => {
        html += `
                <div class="result-item">
                    <div class="chunk-section">Section: ${chunk.metadata.section}</div>
                    <div class="chunk-text">${chunk.text}</div>
                    ${chunk.distance ? `<div style="margin-top: 10px; color: #999; font-size: 0.9em;">Relevance: ${(1 - chunk.distance).toFixed(3)}</div>` : ''}
                </div>
                `;
    });

    resultsContainer.innerHTML = html;
}

// Allow Enter key for query
queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        queryBtn.click();
    }
});
