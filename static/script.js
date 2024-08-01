document.addEventListener('DOMContentLoaded', function () {
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const modelSelect = document.getElementById('model-select');
    const newConversationBtn = document.getElementById('new-conversation-btn');
    const conversationList = document.getElementById('conversation-list');
    const chatSection = document.getElementById('chat-section');
    const conversationCount = document.getElementById('conversation-count');
    const settingsIcon = document.getElementById('settings-btn');
    const settingsPanel = document.getElementById('settings-panel');
    const chatInterface = document.getElementById('chat-interface');

    let conversationCounter = 1;

    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        chatSection.scrollTop = chatSection.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        const model = modelSelect.value;
        if (message) {
            displayMessage(message, 'user');
            fetch('/get-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message, model: model })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    displayMessage(`(${data.model}) ${data.message}`, 'bot');
                })
                .catch((error) => {
                    console.error('Error:', error);
                    displayMessage('Error: Unable to get response', 'bot');
                });
            userInput.value = '';
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function createConversationElement(id, title, date) {
        const newConversation = document.createElement('div');
        newConversation.className = 'conversation';
        newConversation.dataset.id = id;

        newConversation.innerHTML = `
            <span class="conversation-title">${title}</span>
            <span class="date">${date}</span>
            <button class="options-btn">⋮</button>
            <div class="options-menu">
                <button class="rename-btn">重新命名</button>
                <button class="delete-btn">刪除</button>
            </div>
        `;

        return newConversation;
    }

    newConversationBtn.addEventListener('click', function () {
        conversationCounter++;
        const currentDate = new Date();
        const formattedDate = `${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}`;

        const newConversation = createConversationElement(conversationCounter, "New Conversation", formattedDate);
        conversationList.appendChild(newConversation);
        updateConversationCount();
        selectConversation(newConversation);
    });

    conversationList.addEventListener('click', function (e) {
        const clickedConversation = e.target.closest('.conversation');
        if (clickedConversation) {
            if (e.target.classList.contains('options-btn')) {
                toggleOptionsMenu(clickedConversation);
            } else if (e.target.classList.contains('rename-btn')) {
                renameConversation(clickedConversation);
            } else if (e.target.classList.contains('delete-btn')) {
                deleteConversation(clickedConversation);
            } else {
                selectConversation(clickedConversation);
            }
        }
    });

    function toggleOptionsMenu(conversationElement) {
        const optionsMenu = conversationElement.querySelector('.options-menu');
        optionsMenu.style.display = optionsMenu.style.display === 'flex' ? 'none' : 'flex';
    }

    function renameConversation(conversationElement) {
        const titleElement = conversationElement.querySelector('.conversation-title');
        const newTitle = prompt("請輸入新的對話名稱:", titleElement.textContent);
        if (newTitle !== null && newTitle.trim() !== "") {
            titleElement.textContent = newTitle.trim();
        }
        toggleOptionsMenu(conversationElement);
    }

    function deleteConversation(conversationElement) {
        if (confirm("確定要刪除這個對話嗎？")) {
            conversationElement.remove();
            updateConversationCount();
            if (conversationElement.classList.contains('active')) {
                const firstConversation = document.querySelector('.conversation');
                if (firstConversation) {
                    selectConversation(firstConversation);
                } else {
                    chatMessages.innerHTML = '<p>沒有對話記錄</p>';
                }
            }
        }
        toggleOptionsMenu(conversationElement);
    }

    function selectConversation(conversationElement) {
        document.querySelectorAll('.conversation').forEach(conv => conv.classList.remove('active'));
        conversationElement.classList.add('active');
        chatMessages.innerHTML = '';  // Clear previous messages
        // Here you would load the messages for the selected conversation
        // For now, we'll just display a placeholder message
        /*displayMessage(`這是對話 #${conversationElement.dataset.id} 的內容`, 'bot');*/

        chatSection.scrollTop = chatSection.scrollHeight;
    }

    function updateConversationCount() {
        const count = document.querySelectorAll('.conversation').length;
        conversationCount.textContent = count;
    }

    // Initialize: select the first conversation (if it exists)
    const firstConversation = document.querySelector('.conversation');
    if (firstConversation) {
        selectConversation(firstConversation);
    }

    // Close other open option menus
    document.addEventListener('click', function (e) {
        if (!e.target.classList.contains('options-btn')) {
            document.querySelectorAll('.options-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });

    settingsIcon.addEventListener('click', function () {
        const isSettingsPanelVisible = settingsPanel.classList.contains('show');
        settingsPanel.classList.toggle('show', !isSettingsPanelVisible);
        settingsPanel.style.display = isSettingsPanelVisible ? 'none' : 'block';
        chatInterface.style.display = isSettingsPanelVisible ? 'block' : 'none';
    });
});