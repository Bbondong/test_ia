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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const text = await response.text();

        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            addMessage("❌ Erreur serveur", "assistant");
            return;
        }

        if (data.error) {
            addMessage("❌ " + data.error, "assistant");
        } else {
            addMessage(data.reply, "assistant");
        }

    } catch (error) {
        addMessage("❌ " + error.message, "assistant");
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Envoyer';
        messageInput.focus();
    }
});

function addMessage(text, role) {
    const div = document.createElement("div");
    div.className = "message " + role;
    div.innerHTML = "<p>" + text + "</p>";
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

messageInput.focus();