import React, { useEffect, useState } from "react";

export default function App() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/live");

    ws.onopen = () => console.log("WebSocket connected");

    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      setMessages((prev) => [msg, ...prev].slice(0, 50));
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Live Events</h2>

      <div style={{ maxHeight: 400, overflow: "auto" }}>
        {messages.map((m, i) => (
          <pre key={i}>{JSON.stringify(m, null, 2)}</pre>
        ))}
      </div>
    </div>
  );
}
