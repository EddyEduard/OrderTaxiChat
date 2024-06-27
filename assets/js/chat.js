// Constructor for a new message.

function Message(phoneNumber, content, type) {
    this.phoneNumber = phoneNumber;
    this.content = content;
    this.type = type;
    this.time = _ => {
        const date = new Date();
        const hour = date.getHours();
        const minutes = date.getMinutes();

        return `${hour < 0 ? '0' + hour : hour}:${minutes < 0 ? '0' + minutes : minutes}`;
    };
    this.html = _ =>
        `<div class="row message-body">
            <div class="col-sm-12 message-main-${this.type == "SEND" ? 'sender' : 'receiver'}">
                <div class="${this.type == "SEND" ? 'sender' : 'receiver'}">
                    <div class="message-text">
                        ${this.content}
                    </div>
                    <span class="message-time pull-right">
                        ${this.time()}
                    </span>
                </div>
            </div>
        </div>`;
}

// Set a cookie.

const setCookie = (name, value) => {
    const expirationDate = new Date();
    expirationDate.setFullYear(expirationDate.getFullYear() + 1);
    const expires = expirationDate.toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}

// Get a cookie.

const getCookie = name => {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.startsWith(name + "="))
            return cookie.substring(name.length + 1);
    }

    return null;
}

// Create the chat client.

const runIDs = [];

const clientChat = (phoneNumber, conversationTag) => {
    const socket = io("/chat");

    // Connect to the server and submit the phone number.

    socket.on("connect", _ => {
        if (phoneNumber)
            socket.emit("connected", { id: socket.id, phoneNumber: phoneNumber });
    });

    // Check when the client loses connection with the server.

    socket.on("disconnect", _ => {
        alert("The connection to the server has been lost. Please refresh the page.");

        socket.emit("disconnected", { phoneNumber: phoneNumber });
    });

    // Check the client connection to the server.

    socket.on("check_connection", customer => {
        socket.emit("is_connection", customer);
    });

    // Get the reply message from the chatbot.

    socket.on("response", data => {
        if (data["phoneNumber"] == phoneNumber && !runIDs.includes(data["id"])) {
            message = new Message("", data["content"], data["type"]);

            runIDs.push(data["id"]);
            conversationTag.append(message.html());
            conversationTag.animate({ scrollTop: conversationTag.height() + 300 }, 1000);
        }
    });
};

$(function () {
    const phoneNumberInput = $("#phoneNumber");
    const messageInput = $("#message");
    const conversationTag = $("#conversation");
    let phoneNumber = getCookie("phoneNumber");
    let message = null;

    // Open the modal for entering the phone number if it does not exist.

    if (!phoneNumber) {
        $("#modal").modal({
            escapeClose: false,
            clickClose: false,
            showClose: false
        });
    } else {
        clientChat(phoneNumber, conversationTag);

        $("#phoneNumberView").text("You: " + phoneNumber);
    }

    // Send the phone number that is being used for the conversation.

    $("#sendPhoneNumber").on("click", _ => {
        phoneNumber = phoneNumberInput.val();

        if (phoneNumber == "")
            alert("Please enter a phone number (can be fake).")
        else if (phoneNumber.length < 10)
            alert("Please enter a phone number of at least 10 digits (can be fake).")
        else {
            fetch("/check_phone_number?phoneNumber=" + phoneNumber)
                .then(response => {
                    if (response.status != "200" && response.status != "403")
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    if (data["status"] == 200) {
                        setCookie("phoneNumber", phoneNumberInput.val());
                        phoneNumber = getCookie("phoneNumber");

                        clientChat(phoneNumber, conversationTag);

                        $("#phoneNumberView").text("You: " + phoneNumber);
                        $(".jquery-modal").hide();
                    } else
                        alert(data["message"]);
                })
                .catch(error => console.error(error));
        }
    });

    // Send a new message to chat.

    $("#send").on("click", _ => {
        if (messageInput.val() != "") {
            message = new Message(phoneNumber, messageInput.val(), "SEND");

            messageInput.val("");
            conversationTag.append(message.html());
            conversationTag.animate({ scrollTop: conversationTag.height() + 300 }, 1000);

            fetch("/send_message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(message)
            })
                .then(response => {
                    if (!response.ok)
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    return response.json();
                })
                .catch(error => console.error(error));
        }
    });
}) 