// Wait for the document to be fully loaded before running the script.
document.addEventListener('DOMContentLoaded', () => {

    // --- Theme (Dark/Light Mode) Toggler ---
    // Select ALL buttons with the 'theme-toggle' class
    const themeToggleBtns = document.querySelectorAll('.theme-toggle');

    const getPreferredTheme = () => {
        return localStorage.getItem('theme') || 'light';
    };

    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        // Update the icon on ALL toggle buttons
        const iconClass = theme === 'dark' ? 'fa-sun' : 'fa-moon';
        themeToggleBtns.forEach(btn => {
            btn.innerHTML = `<i class="fas ${iconClass}"></i>`;
        });
    };

    // Set the initial theme on page load
    setTheme(getPreferredTheme());

    // Add a click event listener to EACH button
    themeToggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    });

    // --- Back to Top Button Logic ---
    const backToTopButton = document.getElementById('back-to-top-btn');

    if (backToTopButton) {
        // Show or hide the button based on scroll position
        window.onscroll = () => {
            if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
                backToTopButton.style.display = "block";
            } else {
                backToTopButton.style.display = "none";
            }
        };

        // Scroll to the top when the button is clicked
        backToTopButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

        // --- Blog Card Rotator Logic ---
    const cardContainer = document.querySelector('.blog-cards-container');
    if (cardContainer) {
        const cards = cardContainer.querySelectorAll('.blog-card');
        let currentCard = 0;

        if (cards.length > 0) {
            setInterval(() => {
                // Remove active class from current card
                cards[currentCard].classList.remove('active');

                // Move to the next card, looping back to the start
                currentCard = (currentCard + 1) % cards.length;

                // Add active class to the new current card
                cards[currentCard].classList.add('active');
            }, 5000); // Change card every 5 seconds (5000 milliseconds)
        }
    }

    AOS.init({
        duration: 800, // Animation duration in milliseconds
        once: true,    // Whether animation should happen only once
        easing: 'ease-in-out', // Type of animation easing
    });
 

    
});