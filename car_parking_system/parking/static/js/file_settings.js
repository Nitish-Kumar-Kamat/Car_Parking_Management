document.addEventListener('DOMContentLoaded', function () {
    const menuLinks = document.querySelectorAll('.menu a');
    const content = document.getElementById('content');

    // CSRF Token Fetching Function
    function getCSRFToken() {
        return document.getElementById('csrf_token').value;
    }

    function loadContent(page) {
        const csrftoken = getCSRFToken();  // Fetch CSRF token before the request
        fetch(`/${page}/`, {
            method: 'GET',  
            headers: {
                'X-Requested-With': 'XMLHttpRequest', 
                'X-CSRFToken': csrftoken,  // Include CSRF Token here
            },
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            content.innerHTML = data.html;  // Replace content dynamically
        })
        .catch((error) => {
            console.error('Error loading page:', error);
            content.innerHTML = '<h1>Error</h1><p>Unable to load content.</p>';
        });
    }

    menuLinks.forEach((link) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();  
            const page = link.getAttribute('data-page');
            loadContent(page);
        });
    });
});
