// InvoExtract - Main Logic

document.addEventListener('DOMContentLoaded', () => {
    // GSAP Animations
    gsap.registerPlugin(ScrollTrigger);

    // Reveal Text Animation
    gsap.utils.toArray('.reveal-text').forEach(text => {
        gsap.from(text, {
            scrollTrigger: {
                trigger: text,
                start: 'top 85%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            y: 30,
            duration: 1,
            ease: 'power3.out'
        });
    });

    // Fade In Animation
    gsap.utils.toArray('.fade-in').forEach(el => {
        gsap.from(el, {
            scrollTrigger: {
                trigger: el,
                start: 'top 90%',
            },
            opacity: 0,
            y: 20,
            duration: 0.8,
            stagger: 0.2
        });
    });

    // File Upload Logic
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const uploadPlaceholder = document.getElementById('upload-placeholder');
    const imagePreview = document.getElementById('image-preview');
    const filenameLabel = document.getElementById('filename');
    const processBtn = document.getElementById('process-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const loader = document.getElementById('loader');
    const resultsArea = document.getElementById('results-area');
    const resultsTbody = document.getElementById('results-tbody');

    let currentFile = null;
    let costChart = null;

    // Drag & Drop Handlers
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (JPG, PNG).');
            return;
        }
        currentFile = file;
        filenameLabel.textContent = file.name;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            uploadPlaceholder.classList.add('hidden');
            filePreview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }

    cancelBtn.addEventListener('click', () => {
        currentFile = null;
        fileInput.value = '';
        uploadPlaceholder.classList.remove('hidden');
        filePreview.classList.add('hidden');
        resultsArea.classList.add('hidden');
    });

    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // UI State: Loading
        loader.classList.remove('hidden');
        resultsArea.classList.add('hidden');
        processBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                displayResults(data);
            }
        } catch (error) {
            console.error('Extraction failed:', error);
            alert('An error occurred during extraction.');
        } finally {
            loader.classList.add('hidden');
            processBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsArea.classList.remove('hidden');
        resultsTbody.innerHTML = '';
        
        const labels = [];
        const totals = [];

        data.line_items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.description || 'N/A'}</td>
                <td>${item.qty || 0}</td>
                <td>${item.unit_price ? item.unit_price.toFixed(2) : '-'}</td>
                <td><strong>${item.total ? item.total.toFixed(2) : '-'}</strong></td>
            `;
            resultsTbody.appendChild(row);

            if (item.description && item.total) {
                labels.push(item.description.substring(0, 20) + '...');
                totals.push(item.total);
            }
        });

        updateChart(labels, totals);

        // Scroll to results
        gsap.to(window, {duration: 1, scrollTo: "#results-area"});
    }

    function updateChart(labels, values) {
        const ctx = document.getElementById('costChart').getContext('2d');
        
        if (costChart) {
            costChart.destroy();
        }

        costChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#6366f1', '#06b6d4', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6'
                    ],
                    borderWidth: 0,
                    hoverOffset: 20
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#9ca3af',
                            padding: 20,
                            font: { size: 12 }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    }
});
