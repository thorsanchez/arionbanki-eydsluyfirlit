import { useState } from "react";

//Chat component tekur inn
interface ChatProps {
  isEnabled: boolean; // hvort skjal hefur verið hlaðið upp
}

function Chat({ isEnabled }: ChatProps) {
  // fylki geymir chat messages
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);

  // textinn sem user skrifar í input fieldið
  const [chatInput, setChatInput] = useState("");

  // Function sem sendir til backend
  const handleChatSend = async () => {
    // athuga hvort það er eitthvað í input og hvort chat er enabled
    if (!chatInput.trim() || !isEnabled) return;

    //bæta user message við messages array
    const userMessage = { role: "user", content: chatInput };
    setMessages(prev => [...prev, userMessage]);

    //hreinsa input field
    setChatInput("");

    try {
      //post request til backend með skilaboð
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: chatInput })
      });

      //json response frá backend
      const data = await response.json();

      // Bæta gemma svar við messages array
      setMessages(prev => [...prev, { role: "assistant", content: data.response }]);
    } catch {
      // Ef eitthvað fer úrskeiðis, sýna error
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "error við að svara"
      }]);
    }
  };

  //fela chat ef það er ekki enabled
  if (!isEnabled) return null;

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>Spyrðu um útgjöldin þín</h2>

      {/* Scrollable box sem sýnir öll messages */}
      <div style={{
        border: "1px solid #ccc",
        padding: "10px",
        height: "300px",
        overflowY: "scroll",
        marginBottom: "10px"
      }}>
        {/* Loopa í gegnum öll messages og sýna þau */}
        {messages.map((msg, i) => (
          <div key={i} style={{
            margin: "10px 0",
            // User hægra megin, assistant vinstra megin
            textAlign: msg.role === "user" ? "right" : "left" 
          }}>
            <strong>{msg.role === "user" ? "Þú" : "Greining"}:</strong>
            <p style={{ whiteSpace: "pre-wrap" }}>{msg.content}</p>
          </div>
        ))}
      </div>

      {/* Input field þar sem user skrifar spurningar */}
      <input
        type="text"
        value={chatInput}
        onChange={(e) => setChatInput(e.target.value)}
        //Leyfa enter takka!
        onKeyDown={(e) => e.key === "Enter" && handleChatSend()}
        placeholder="t.d. Hvað kostaði matur í desember?"
        style={{ width: "70%", padding: "8px" }}
      />
      <button onClick={handleChatSend}>Senda</button>
    </div>
  );
}

export default Chat;
