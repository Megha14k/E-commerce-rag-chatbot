const API_URL = "http://127.0.0.1:8000/chat";

function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}

function addMessage(text, sender, sources = []) {
    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.className = sender === "user"
        ? "chat-message user-message"
        : "chat-message bot-message";

    let html = `<div>${escapeHtml(text)}</div>`;

    if (sources.length > 0) {
        html += `<div class="source-box"><strong>Sources:</strong><br>`;

        sources.forEach((src, index) => {
            const name = escapeHtml(src.name || "Unknown");
            const price = escapeHtml(src.price || "");
            const url = src.url || "#";

            html += `
                ${index + 1}. ${name} - ${price}
                <br>
                <a href="${url}" target="_blank">View product</a><br>
            `;
        });

        html += `</div>`;
    }

    div.innerHTML = html;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function fillQuestion(text) {
    document.getElementById("question").value = text;
    document.getElementById("question").focus();

    const chatbotSection = document.getElementById("chatbot");
    if (chatbotSection) {
        chatbotSection.scrollIntoView({ behavior: "smooth" });
    }
}

async function sendMessage() {
    const input = document.getElementById("question");
    const button = document.getElementById("send-btn");
    const question = input.value.trim();

    if (!question) return;

    addMessage(question, "user");
    input.value = "";
    button.disabled = true;
    button.innerText = "Thinking...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();

        addMessage(
            data.answer || "No answer returned.",
            "bot",
            data.sources || []
        );

    } catch (error) {
        addMessage(
            "Could not connect to backend API. Make sure FastAPI is running on http://127.0.0.1:8000",
            "bot"
        );
    }

    button.disabled = false;
    button.innerText = "Send";
}

function handleEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}