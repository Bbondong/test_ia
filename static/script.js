const messageInput = document.getElementById('messageInput');
const chatForm = document.getElementById('chatForm');
const messagesContainer = document.getElementById('messages');
const sendBtn = document.getElementById('sendBtn');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    messageInput.value = '';

    sendBtn.disabled = true;
    sendBtn.textContent = 'Envoi...';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.error) {
            addMessage(`❌ ${data.error}`, 'assistant');
        } else {
            addMessage(data.reply, 'assistant');
        }
    } catch (error) {
        addMessage(`❌ Erreur: ${error.message}`, 'assistant');
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Envoyer';
        messageInput.focus();
    }
});

function addMessage(text, role) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.innerHTML = `<p>${text}</p>`;
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

messageInput.focus();
