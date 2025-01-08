document.addEventListener('DOMContentLoaded', () => {
    // Define available themes
    const themes = ["lofi", "black"];

    // Select the theme toggle input
    const themeToggle = document.querySelector('.theme-controller');
    const body = document.body;

    // Initialize theme from localStorage or default to the first theme
    const savedTheme = localStorage.getItem('theme') || themes[0];
    body.setAttribute('data-theme', savedTheme);

    // Set the initial state of the toggle based on the saved theme
    if (savedTheme === themes[1]) {
        themeToggle.checked = true;
    }

    // Add event listener to handle theme switching
    themeToggle.addEventListener('change', () => {
        // Determine the new theme based on toggle state
        const newTheme = themeToggle.checked ? themes[1] : themes[0];
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Cookie consent functionality
    const cookieModal = document.querySelector('#cookie-consent'); // Select the modal element
    const acceptCookiesButton = cookieModal.querySelector('.btn'); // Select the accept button

    // Check if cookies have already been accepted
    const cookiesAccepted = localStorage.getItem('cookiesAccepted');

    if (cookiesAccepted) {
        // Hide the modal if cookies have been accepted
        cookieModal.style.display = 'none';
    }

    // Add event listener to the accept button
    acceptCookiesButton.addEventListener('click', () => {
        // Save the cookie acceptance in localStorage
        localStorage.setItem('cookiesAccepted', true);

        // Hide the modal
        cookieModal.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const squareContainer = document.getElementById('floating-squares');

    function createSquare() {
        const square = document.createElement('div');
        const size = Math.random() * 10 + 10; // Random size between 10px and 20px
        const position = Math.random() * 100; // Random horizontal position
        const animationDuration = Math.random() * 3 + 3; // Random duration between 3s and 6s
        const theme = document.body.getAttribute('data-theme');
        const squareColor = theme === 'lofi' ? 0 : 255;

        square.style.width = `${size}px`;
        square.style.height = `${size}px`;
        square.style.position = 'absolute';
        square.style.bottom = '-20px';
        square.style.left = `${position}%`;
        square.style.backgroundColor = `rgba(${squareColor}, ${squareColor}, ${squareColor}, ${Math.random() * 0.8 + 0.2})`;
        square.style.borderRadius = '3px';
        square.style.animation = `rise ${animationDuration}s linear infinite`;

        squareContainer.appendChild(square);

        // Remove square after animation ends
        setTimeout(() => {
            square.remove();
        }, animationDuration * 1000);
    }

    // Generate squares at regular intervals
    setInterval(createSquare, 300);
});

