document.getElementById('queryForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const question = formData.get('question');
    
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('errorMessage');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    loadingDiv.classList.remove('hidden');
    errorDiv.classList.add('hidden');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/query/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            window.location.href = `/results/${data.report_id}`;
        } else {
            if (response.status === 401) {
                window.location.href = '/login';
            } else {
                errorDiv.textContent = data.detail || 'Failed to submit query';
                errorDiv.classList.remove('hidden');
                loadingDiv.classList.add('hidden');
                submitBtn.disabled = false;
            }
        }
    } catch (error) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.remove('hidden');
        loadingDiv.classList.add('hidden');
        submitBtn.disabled = false;
    }
});
