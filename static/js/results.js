const reportId = window.location.pathname.split('/').pop();

async function loadReport() {
    const loadingDiv = document.getElementById('loading');
    const contentDiv = document.getElementById('reportContent');
    const errorDiv = document.getElementById('errorMessage');
    
    try {
        const response = await fetch(`/api/results/${reportId}`);
        
        if (response.ok) {
            const data = await response.json();
            
            document.getElementById('reportTitle').textContent = data.title;
            document.getElementById('reportQuestion').textContent = `Query: ${data.question}`;
            document.getElementById('reportDate').textContent = `Generated: ${new Date(data.created_at).toLocaleString()}`;
            
            const reportTextDiv = document.getElementById('reportText');
            reportTextDiv.innerHTML = marked.parse ? marked.parse(data.report_text) : data.report_text;
            
            loadingDiv.classList.add('hidden');
            contentDiv.classList.remove('hidden');
        } else {
            if (response.status === 401) {
                window.location.href = '/login';
            } else {
                loadingDiv.classList.add('hidden');
                errorDiv.textContent = 'Failed to load report';
                errorDiv.classList.remove('hidden');
            }
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        errorDiv.textContent = 'An error occurred while loading the report';
        errorDiv.classList.remove('hidden');
    }
}

function downloadPDF() {
    alert('PDF download feature will be implemented in future updates');
}

loadReport();
