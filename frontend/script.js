const chatBox = document.getElementById('chat-box');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const showHistoryBtn = document.getElementById('show-history');
const clearMemoryBtn = document.getElementById('clear-memory');

function appendMessage(who, text) {
  const div = document.createElement('div');
  div.className = 'message ' + (who === 'user' ? 'msg-user' : 'msg-bot');
  if (text && text.includes('```')) {
    const parts = text.split('```');
    for (let i=0;i<parts.length;i++){
      if (i % 2 === 0){
        const p = document.createElement('div');
        p.textContent = parts[i];
        div.appendChild(p);
      } else {
        const pre = document.createElement('pre');
        pre.textContent = parts[i];
        div.appendChild(pre);
      }
    }
  } else {
    div.textContent = text;
  }
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(message) {
  appendMessage('user', message);
  try {
    const res = await fetch('http://127.0.0.1:9000/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message})
    });
    if (!res.ok) {
      appendMessage('bot', 'Error: backend returned ' + res.status);
      return;
    }
    const data = await res.json();
    appendMessage('bot', data.reply || data.response || 'No response');
  } catch (e) {
    appendMessage('bot', 'Network error: ' + e.message);
  }
}

form.addEventListener('submit', e => {
  e.preventDefault();
  const v = input.value.trim();
  if (!v) return;
  sendMessage(v);
  input.value = '';
});

showHistoryBtn.addEventListener('click', async () => {
  try {
    const res = await fetch('http://127.0.0.1:9000/history');
    const data = await res.json();
    if (!data.recent || data.recent.length === 0) {
      appendMessage('bot', 'Memory is empty.');
      return;
    }
    appendMessage('bot', '--- Recent memory ---');
    data.recent.forEach(e => {
      appendMessage('bot', `You: ${e.user}\nDexa: ${e.bot}`);
    });
  } catch (e) {
    appendMessage('bot', 'Error fetching history: ' + e.message);
  }
});

clearMemoryBtn.addEventListener('click', async () => {
  try {
    const res = await fetch('http://127.0.0.1:9000/clear', {method: 'POST'});
    const data = await res.json();
    appendMessage('bot', data.message || 'Memory cleared.');
  } catch (e) {
    appendMessage('bot', 'Error clearing memory: ' + e.message);
  }
});
