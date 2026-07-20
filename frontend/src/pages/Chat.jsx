import { useState, useEffect, useRef } from "react";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function Chat() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState("");
  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (activeSessionId) loadMessages(activeSessionId);
  }, [activeSessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadSessions = async () => {
    try {
      const res = await api.get("/chat/sessions");
      setSessions(res.data);
      if (res.data.length > 0) setActiveSessionId(res.data[0].id);
    } catch (err) {
      if (err.response?.status === 401) {
        logout();
        navigate("/login");
      }
    }
  };

  const loadMessages = async (sessionId) => {
    const res = await api.get(`/chat/${sessionId}/messages`);
    setMessages(res.data.messages);
  };

  const createSession = async () => {
    const title = prompt("Session title:") || "New Chat";
    const res = await api.post("/chat/session", { title });
    setSessions((prev) => [res.data, ...prev]);
    setActiveSessionId(res.data.id);
    setMessages([]);
  };

  const deleteSession = async (id, e) => {
    e.stopPropagation();
    if (!confirm("Delete this session?")) return;

    await api.delete(`/chat/session/${id}`);

    setSessions((prev) => prev.filter((s) => s.id !== id));

    if (activeSessionId === id) {
      setActiveSessionId(null);
      setMessages([]);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim() || !activeSessionId) return;

    const userMsg = {
      id: Date.now(),
      sender: "user",
      message: input,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setSending(true);

    try {
      const res = await api.post(
        `/chat/${activeSessionId}/message`,
        { message: userMsg.message }
      );

      setMessages((prev) => [...prev, res.data]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: "assistant",
          message: "Error: could not get response.",
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  // ================= MULTIPLE PDF UPLOAD =================

  const handleUpload = async (e) => {
    const files = e.target.files;

    if (!files || files.length === 0) return;

    setUploading(true);
    setUploadMsg("");

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      const res = await api.post("/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (res.data.error) {
        setUploadMsg(`⚠️ ${res.data.error}`);
      } else {
        setUploadMsg(
          `✅ ${res.data.total_files} PDFs indexed (${res.data.total_chunks} chunks)`
        );
      }
    } catch (err) {
      setUploadMsg("❌ Upload failed");
    } finally {
      setUploading(false);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="chat-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>Healthcare AI</h2>

          <button
            className="icon-btn"
            onClick={handleLogout}
            title="Logout"
          >
            ⏻
          </button>
        </div>

        <button className="new-chat-btn" onClick={createSession}>
          + New Chat
        </button>

        <div className="upload-section">

          <input
            type="file"
            accept="application/pdf"
            multiple
            ref={fileInputRef}
            onChange={handleUpload}
            id="pdf-upload"
            hidden
          />

          <label htmlFor="pdf-upload" className="upload-btn">
            {uploading ? "Uploading..." : "📚 Upload PDFs"}
          </label>

          {uploadMsg && (
            <p className="upload-status">{uploadMsg}</p>
          )}
        </div>

        <div className="sessions-list">
          {sessions.map((s) => (
            <div
              key={s.id}
              className={`session-item ${
                s.id === activeSessionId ? "active" : ""
              }`}
              onClick={() => setActiveSessionId(s.id)}
            >
              <span>{s.title}</span>

              <button
                className="delete-btn"
                onClick={(e) => deleteSession(s.id, e)}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </aside>

      <main className="chat-main">
        {!activeSessionId ? (
          <div className="empty-state">
            <p>Create a new chat to get started</p>
          </div>
        ) : (
          <>
            <div className="messages-area">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={`message ${m.sender}`}
                >
                  <div className="message-bubble">
                    {m.message}
                  </div>
                </div>
              ))}

              {sending && (
                <div className="message assistant">
                  <div className="message-bubble typing">
                    Thinking...
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <form className="input-area" onSubmit={sendMessage}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask something about your uploaded documents..."
                disabled={sending}
              />

              <button
                type="submit"
                disabled={sending || !input.trim()}
              >
                Send
              </button>
            </form>
          </>
        )}
      </main>
    </div>
  );
}

export default Chat;