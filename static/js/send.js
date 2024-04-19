function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    var chatMessages = document.getElementById("chat-messages");

    // Add user's message to chat
    var userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.textContent = userInput;
    chatMessages.appendChild(userMessage);

    // Simulate bot response (replace this with actual bot response)
    var botResponse = document.createElement("div");
    botResponse.classList.add("message", "bot-message");
    botResponse.textContent = "This is a bot response.";
    chatMessages.appendChild(botResponse);

    // Clear input field after sending message
    document.getElementById("user-input").value = "";

    // Scroll to bottom of chat messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Event listener for send button
document.getElementById("send-button").addEventListener("click", sendMessage);