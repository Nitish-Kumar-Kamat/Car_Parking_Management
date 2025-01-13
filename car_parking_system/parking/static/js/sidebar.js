 // Sidebar Toggle Button Functionality
 document.getElementById('toggle-btn').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('minimized');
});

document.addEventListener('DOMContentLoaded', function () {
    const menuLinks = document.querySelectorAll('.menu a');
    const content = document.getElementById('content');
   
    function loadContent(page) {
        fetch(`/${page}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Indicate it's an AJAX request
                
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                content.innerHTML = data.html; // Replace content dynamically
            })
            .catch((error) => {
                console.error('Error loading page:', error);
                content.innerHTML = '<h1>Error</h1><p>Unable to load content.</p>';
            });
    }

    menuLinks.forEach((link) => {
        link.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default link behavior
            const page = link.getAttribute('data-page');
            loadContent(page);
        });
    });
});
