
    function convertToHTML(inputText) {
        console.log("convert ed");
        let boldText = inputText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // 替换换行为 <br>
        let htmlText = boldText.replace(/\n/g, '<br>');

        return htmlText;
    }

// JavaScript function to add a new message to the chat
    function addMessage(message, sentByUser) {
        message = convertToHTML(message);
        const messageContainer = document.getElementById('messageContainer');
        const messageElement = document.createElement('div');
        messageElement.innerHTML = message;
        messageElement.classList.add('message');
        if (sentByUser) {
            messageElement.classList.add('sent');
        } else {
            messageElement.classList.add('received');
        }
        // Insert the new message at the bottom of the message container
        //messageContainer.insertBefore(messageElement, messageContainer.firstChild);
        messageContainer.appendChild(messageElement);
        // Scroll to the bottom of the message container
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Add some example messages
//    addMessage("Hello!", false); // Received message
//    addMessage("Hi there!", true); // Sent message
//    addMessage("How are you?", false); // Received message
//    addMessage("I'm doing well, thank you!", true); // Sent message
//    addMessage("That's good to hear!", false); // Received message

