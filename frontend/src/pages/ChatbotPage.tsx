// 📄 src/pages/ChatbotPage.tsx
import React, { useState } from "react";

const ChatbotPage = () => {
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const newMessages = [...messages, { role: "user", text: userInput }];
    setMessages(newMessages);
    setUserInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
      });

      const data = await res.json();
      setMessages([...newMessages, { role: "ai", text: data.response }]);
    } catch (err) {
      setMessages([...newMessages, { role: "ai", text: "❌ 쳭8볼 응답 실패" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "2rem",
        boxSizing: "border-box",
        backgroundColor: "#fff",
        position: "relative",
      }}
    >
      <h2 style={{ fontSize: "2rem", marginBottom: "1rem" }}>💬 장학금 ChatBOT
      </h2>

      <div
        style={{
          width: "100%",
          maxWidth: "700px",
          height: "60vh",
          overflowY: "auto",
          border: "1px solid #ddd",
          borderRadius: "8px",
          padding: "1rem",
          marginBottom: "1rem",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{ textAlign: msg.role === "user" ? "right" : "left", marginBottom: "1rem" }}
          >
            <strong>{msg.role === "user" ? "🙋‍♀️" : "🤖"}</strong>
            <div>{msg.text}</div>
          </div>
        ))}
      </div>

      <div style={{ width: "100%", maxWidth: "700px", display: "flex" }}>
        <input
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={{ flex: 1, padding: "0.8rem", fontSize: "1rem" }}
          placeholder="질문을 입력하세요..."
        />
        <button
          onClick={handleSend}
          disabled={loading}
          style={{
            padding: "0.8rem 1.5rem",
            fontSize: "1rem",
            border: "none",
            backgroundColor: "#f3f3f3",
            marginLeft: "0.5rem",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          {loading ? "전송 중..." : "전송"}
        </button>
      </div>

      <p
        style={{
          position: "absolute",
          bottom: "1rem",
          fontSize: "0.8rem",
          color: "#aaa",
        }}
      >
        Ⓜ 2025 JARVIS Corp.
      </p>
    </div>
  );
};

export default ChatbotPage;
