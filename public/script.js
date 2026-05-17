const messageInput = document.getElementById('messageInput');
const chatForm = document.getElementById('chatForm');
const messagesContainer = document.getElementById('messages');
const sendBtn = document.getElementById('sendBtn');
const spinner = document.getElementById('spinner');

const API_ENDPOINT = '/api/chat';

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessageToChat(message, 'user');
    messageInput.value = '';

    // Disable send button and show spinner
    sendBtn.disabled = true;
    spinner.classList.remove('hidden');

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            addMessageToChat(`❌ Erreur: ${data.error}`, 'assistant');
        } else {
            addMessageToChat(data.reply, 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat(
            `❌ Erreur de connexion: ${error.message}\n\nVérifiez que le backend est en ligne et que l'API token est configuré.`,
            'assistant',
            true
        );
    } finally {
        sendBtn.disabled = false;
        spinner.classList.add('hidden');
        messageInput.focus();
    }
});

function addMessageToChat(text, role, isError = false) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;

    const contentEl = document.createElement('div');
    contentEl.className = `message-content ${isError ? 'error-message' : ''}`;
    contentEl.textContent = text;

    messageEl.appendChild(contentEl);
    messagesContainer.appendChild(messageEl);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Focus on input when page loads
messageInput.focus();

// Auto-resize input on mobile
const originalHeight = messageInput.offsetHeight;
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});
