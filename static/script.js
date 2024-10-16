document.addEventListener('DOMContentLoaded', function () {
    const modelSelectHeader = document.querySelector('.model-select-header');
    const modelSelectDropdown = document.querySelector('.model-select-dropdown');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const newConversationBtn = document.getElementById('new-conversation-btn');
    const conversationList = document.getElementById('conversation-list');
    const chatSection = document.getElementById('chat-section');
    const conversationCount = document.getElementById('conversation-count');
    const settingsIcon = document.getElementById('settings-btn');
    const settingsPanel = document.getElementById('settings-panel');
    const chatInterface = document.getElementById('chat-interface');
    const noConversationMessage = document.getElementById('no-conversation-message');
    const fileUpload = document.getElementById('file-upload');
    const uploadButton = document.getElementById('upload-button');
    const confirmUpload = document.getElementById('confirm-upload');
    const fileList = document.getElementById('file-list');
    const uploadStatus = document.getElementById('upload-status');
    const uploadedFilesList = document.getElementById('uploaded-files-list');

    let conversationCounter = 0;
    let conversations = {};
    let filesToUpload = [];

    modelSelectHeader.addEventListener('click', function () {
        modelSelectDropdown.style.display = modelSelectDropdown.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function (event) {
        if (!event.target.closest('.model-select-container')) {
            modelSelectDropdown.style.display = 'none';
        }
    });

    function updateSelectedModelsDisplay() {
        const selectedModels = Array.from(document.querySelectorAll('.model-select-dropdown input:checked'))
            .map(checkbox => checkbox.value);
        modelSelectHeader.textContent = selectedModels.length > 0
            ? `▲ ${selectedModels.length} Models Selected`
            : '▲ Please Select Model';
    }

    document.querySelectorAll('.model-select-dropdown input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedModelsDisplay);
    });

    function getSelectedModels() {
        return Array.from(document.querySelectorAll('.model-select-dropdown input:checked'))
            .map(checkbox => checkbox.value);
    }

    function displayMessage(message, sender, model = '') {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        const parsedMessage = marked.parse(message);
        if (model) {
            messageElement.innerHTML = `<strong>(${model})</strong><br> ${parsedMessage}`;
        } else {
            messageElement.innerHTML = parsedMessage;
        }
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        chatSection.scrollTop = chatSection.scrollHeight;
    }

    function sendMessage() {
        const message = userInput.value.trim();
        const selectedModels = getSelectedModels();
        if (message && selectedModels.length > 0) {
            const activeConversationId = document.querySelector('.conversation.active')?.dataset.id;
            if (activeConversationId) {
                displayMessage(message, 'user');
                conversations[activeConversationId].push({ sender: 'user', content: message });

                selectedModels.forEach(model => {
                    fetch('/get-response', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: message, model: model, format: 'markdown' })
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Success:', data);
                            displayMessage(data.message, 'bot', data.model);
                            conversations[activeConversationId].push({ sender: 'bot', content: data.message, model: data.model });
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                            displayMessage('Error: Unable to get response', 'bot', model);
                            conversations[activeConversationId].push({ sender: 'bot', content: 'Error: Unable to get response', model: model });
                        });
                });
                userInput.value = '';
            }
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

        conversations[id] = [];
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
        updateChatDisplay();
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
            const conversationId = conversationElement.dataset.id;
            delete conversations[conversationId];
            conversationElement.remove();
            updateConversationCount();
            if (conversationElement.classList.contains('active')) {
                const firstConversation = document.querySelector('.conversation');
                if (firstConversation) {
                    selectConversation(firstConversation);
                } else {
                    chatMessages.innerHTML = '';
                }
            }
            updateChatDisplay();
        }
        toggleOptionsMenu(conversationElement);
    }

    function selectConversation(conversationElement) {
        document.querySelectorAll('.conversation').forEach(conv => conv.classList.remove('active'));
        conversationElement.classList.add('active');
        chatMessages.innerHTML = '';
        const conversationId = conversationElement.dataset.id;
        const messages = conversations[conversationId] || [];
        messages.forEach(msg => displayMessage(msg.content, msg.sender, msg.model));
        chatSection.scrollTop = chatSection.scrollHeight;
        updateChatDisplay();
    }

    function updateConversationCount() {
        const count = document.querySelectorAll('.conversation').length;
        conversationCount.textContent = count;
    }

    function updateChatDisplay() {
        const conversations = document.querySelectorAll('.conversation');
        if (conversations.length === 0) {
            noConversationMessage.style.display = 'block';
            chatSection.style.display = 'none';
        } else {
            noConversationMessage.style.display = 'none';
            chatSection.style.display = 'block';
        }
    }

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
        if (!isSettingsPanelVisible) {
            fetchAndDisplayUploadedFiles();
        }
    });

    updateChatDisplay();

    uploadButton.addEventListener('click', function () {
        fileUpload.click();
    });

    fileUpload.addEventListener('change', function () {
        filesToUpload = Array.from(fileUpload.files);
        updateFileList();
        confirmUpload.style.display = 'inline-block';
        uploadStatus.textContent = '';
    });

    function updateFileList() {
        fileList.innerHTML = '';
        filesToUpload.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.textContent = file.name;
            fileList.appendChild(fileItem);
        });
    }

    confirmUpload.addEventListener('click', function () {
        if (filesToUpload.length > 0) {
            uploadFiles(filesToUpload);
        }
    });

    function uploadFiles(files) {
        uploadStatus.textContent = 'Loading...';

        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                uploadStatus.textContent = 'Files uploaded successfully!';
                filesToUpload = [];
                updateFileList();
                confirmUpload.style.display = 'none';
                fetchAndDisplayUploadedFiles();
            })
            .catch(error => {
                uploadStatus.textContent = 'Error uploading files.';
                console.error('Error:', error);
            });
    }

    function fetchAndDisplayUploadedFiles() {
        showLoading(true);
        fetch('/list-files')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayUploadedFiles(data.files);
                    // 確保上傳按鈕和文件輸入框處於正確狀態
                    resetFileUploadState();
                } else {
                    console.error('Error fetching files:', data.message);
                    alert('獲取文件列表失敗，請刷新頁面重試');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('獲取文件列表時發生錯誤，請刷新頁面重試');
            })
            .finally(() => {
                showLoading(false);
            });
    }

    function displayUploadedFiles(files) {
        uploadedFilesList.innerHTML = '';
        files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'uploaded-file-item';
            fileItem.innerHTML = `
            <span>${file.name}</span>
            <button class="delete-file-btn" data-file-id="${file.id}">Delete</button>
        `;
            uploadedFilesList.appendChild(fileItem);
        });
    }

    function deleteFile(fileId) {
        showLoading(true);
        fetch(`/delete-file/${fileId}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    removeFileFromUI(fileId);
                    alert('文件刪除成功');
                    // 重置文件上傳相關的狀態
                    resetFileUploadState();
                } else {
                    alert(`刪除文件失敗: ${data.message}`);
                    console.error('Error deleting file:', data.message);
                }
            })
            .catch(error => {
                alert('刪除文件時發生錯誤，請稍後再試');
                console.error('Error:', error);
            })
            .finally(() => {
                showLoading(false);
                fetchAndDisplayUploadedFiles();
            });
    }

    function resetFileUploadState() {
        filesToUpload = [];
        fileUpload.value = ''; // 重置文件輸入
        updateFileList();
        confirmUpload.style.display = 'none';
        uploadStatus.textContent = '';
    }

    function removeFileFromUI(fileId) {
        const fileElement = document.querySelector(`[data-file-id="${fileId}"]`);
        if (fileElement) {
            fileElement.closest('.uploaded-file-item').remove();
        }
    }

    function showLoading(isLoading) {
        // 實現顯示/隱藏 loading 指示器的邏輯
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = isLoading ? 'block' : 'none';
        }
    }

    uploadedFilesList.addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-file-btn')) {
            const fileId = e.target.dataset.fileId;
            if (confirm('確定要刪除這個文件嗎？')) {
                deleteFile(fileId);
            }
        }
    });
});