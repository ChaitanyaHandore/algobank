// Main JavaScript file for AlgoBank
// Additional functionality can be added here

document.addEventListener('DOMContentLoaded', function() {
    // Any global initialization code
    console.log('AlgoBank loaded');
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.result-message, .result-box');
    flashMessages.forEach(msg => {
        if (msg.textContent.includes('successful') || msg.textContent.includes('✓')) {
            setTimeout(() => {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s';
                setTimeout(() => msg.remove(), 500);
            }, 5000);
        }
    });
});

