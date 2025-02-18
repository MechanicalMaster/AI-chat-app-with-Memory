// Theme handling
let isDarkMode = true;

function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    document.body.classList.toggle('light-mode');
    
    const themeIcon = document.querySelector('.btn-theme i');
    themeIcon.classList.toggle('fa-moon');
    themeIcon.classList.toggle('fa-sun');
    
    // Save preference
    localStorage.setItem('darkMode', isDarkMode);
}

// Initialize theme from saved preference
document.addEventListener('DOMContentLoaded', () => {
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'false') {
        toggleTheme();
    }
    
    // Focus input on load
    document.getElementById('user-input').focus();
});

// Message handling
async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Disable input while processing
    input.value = '';
    input.disabled = true;
    
    // Add user message
    appendMessage(message, 'user');
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        const data = await response.json();
        appendMessage(data.response, 'assistant');
    } catch (error) {
        appendMessage('Sorry, there was an error processing your request.', 'assistant error');
    }
    
    // Re-enable input
    input.disabled = false;
    input.focus();
}

function appendMessage(content, type) {
    const container = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${type}-message`);
    messageDiv.textContent = content;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function clearChat() {
    const container = document.getElementById('chat-container');
    container.innerHTML = `
        <div class="message assistant-message">
            Hello! I'm your Channel Finance assistant. How can I help you with loan-related questions today?
        </div>
    `;
}

// Add smooth scrolling for iOS
document.documentElement.style.scrollBehavior = 'smooth';