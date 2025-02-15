class ChatApp {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.messageContainer = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.clearButton = document.getElementById('clear-chat');
        this.themeToggle = document.getElementById('theme-toggle');
        this.isWaitingForResponse = false;
        
        this.setupEventListeners();
        this.loadTheme();
        this.displayWelcomeMessage();
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        this.clearButton.addEventListener('click', () => this.clearChat());
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }

    loadTheme() {
        const isDarkTheme = localStorage.getItem('darkTheme') === 'true';
        if (isDarkTheme) {
            document.body.classList.add('dark-theme');
            this.themeToggle.innerHTML = '<i class="fas fa-sun"></i> Toggle Theme';
        }
    }

    toggleTheme() {
        document.body.classList.toggle('dark-theme');
        const isDarkTheme = document.body.classList.contains('dark-theme');
        localStorage.setItem('darkTheme', isDarkTheme);
        this.themeToggle.innerHTML = isDarkTheme ? 
            '<i class="fas fa-sun"></i> Toggle Theme' : 
            '<i class="fas fa-moon"></i> Toggle Theme';
    }

    displayWelcomeMessage() {
        const welcomeMessage = "Hello! I'm your Channel Finance assistant. How can I help you with loan-related questions today?";
        this.addMessage(welcomeMessage, 'assistant');
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        this.messageContainer.appendChild(typingDiv);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
        return typingDiv;
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isWaitingForResponse) return;

        this.isWaitingForResponse = true;
        this.userInput.value = '';
        this.sendButton.disabled = true;

        // Display user message
        this.addMessage(message, 'user');
        const typingIndicator = this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            typingIndicator.remove();

            const data = await response.json();
            if (response.ok) {
                this.addMessage(data.response, 'assistant');
            } else {
                throw new Error(data.detail || 'Something went wrong');
            }
        } catch (error) {
            typingIndicator.remove();
            this.addMessage('Sorry, there was an error processing your request.', 'assistant');
            console.error('Error:', error);
        } finally {
            this.isWaitingForResponse = false;
            this.sendButton.disabled = false;
            this.userInput.focus();
        }
    }

    async clearChat() {
        try {
            await fetch(`/api/clear/${this.sessionId}`, { method: 'POST' });
            this.messageContainer.innerHTML = '';
            this.displayWelcomeMessage();
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }

    addMessage(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${role}-message`);
        messageDiv.textContent = content;
        this.messageContainer.appendChild(messageDiv);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}

// Initialize the chat app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApp();
}); 