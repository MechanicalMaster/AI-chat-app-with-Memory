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
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
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

document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const themeToggle = document.getElementById('themeToggle');
    const clearChat = document.getElementById('clearChat');
    const sessionId = Date.now().toString();

    // Add initial welcome message
    appendMessage("Hello! I'm your Channel Finance assistant. How can I help you with loan-related questions today?", 'assistant');

    // Theme Management
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.body.className = currentTheme + '-theme';
    updateThemeIcon();

    function updateThemeIcon() {
        const icon = themeToggle.querySelector('i');
        if (document.body.className.includes('light')) {
            icon.className = 'fas fa-moon';
        } else {
            icon.className = 'fas fa-sun';
        }
    }

    // Chat Functions
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            if (data.error) {
                appendMessage('Error: ' + data.error, 'assistant');
            } else {
                appendMessage(data.response, 'assistant');
            }
        } catch (error) {
            appendMessage('Error: Could not connect to the server', 'assistant');
        }
    }

    function appendMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
        setTimeout(() => {
            messageDiv.classList.add('show');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 100);
    }

    // Event Listeners
    themeToggle.addEventListener('click', () => {
        const newTheme = document.body.className.includes('light') ? 'dark' : 'light';
        document.body.className = newTheme + '-theme';
        localStorage.setItem('theme', newTheme);
        updateThemeIcon();
    });

    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    clearChat.addEventListener('click', async () => {
        try {
            await fetch(`/clear/${sessionId}`, { method: 'POST' });
            chatContainer.innerHTML = '';
            appendMessage("Hello! I'm your Channel Finance assistant. How can I help you with loan-related questions today?", 'assistant');
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    });

    // Focus input on load
    userInput.focus();
});