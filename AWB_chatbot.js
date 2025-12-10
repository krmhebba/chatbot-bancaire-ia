const toggleBtn = document.getElementById('themeToggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const savedTheme = localStorage.getItem('theme');
let currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    toggleBtn.textContent = theme === 'dark' ? '☀️ Mode clair' : '🌙 Mode sombre';
    localStorage.setItem('theme', theme);
}

applyTheme(currentTheme);

toggleBtn.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme);
});

const chatbox = document.getElementById('chatbox');
const input = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

function sendMessage() {
    const message = input.value.trim();
    if (message === '') return;
    
    appendMessage('user', message);
    input.value = '';
    
    const thinkingIndicator = document.createElement('div');
    thinkingIndicator.className = 'thinking';
    thinkingIndicator.id = 'thinking';
    thinkingIndicator.textContent = 'En cours...';
    chatbox.appendChild(thinkingIndicator);
    chatbox.scrollTop = chatbox.scrollHeight;
    
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('thinking').remove();
        appendMessage('assistant', data.reponse);
    })
    .catch(error => {
        document.getElementById('thinking').remove();
        appendMessage('assistant', "Erreur de connexion.");
    });
}

function appendMessage(role, text) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${role}`;
    messageElement.innerHTML = role === 'assistant' ? `<strong>Assistant:</strong> ${text}` : text;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}

sendButton.addEventListener('click', sendMessage);
input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});