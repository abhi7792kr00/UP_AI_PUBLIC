import { useState } from "react";
import { Bot, Mic, Send, Sparkles, UserRound } from "lucide-react";
import { Button, Card, Input } from "../components/ui";

type Message = { role: "ai" | "user"; text: string };

export function AIPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", text: "Namaste! Main UP_AI Assistant hoon. Aap complaint tracking, officers, departments ya government services ke baare mein pooch sakte hain." },
  ]);

  const send = () => {
    if (!input.trim()) return;
    const question = input.trim();
    setMessages(m => [...m, { role: "user", text: question }, { role: "ai", text: "Demo response: Backend AI Gateway connect hone ke baad main real UP_AI data, RAG sources aur tool-calling results ke saath answer dunga." }]);
    setInput("");
  };

  return <div className="ai-page">
    <div className="ai-shell">
      <div className="ai-header"><div className="ai-orb"><Bot size={24}/></div><div><div className="eyebrow">UP_AI ASSISTANT</div><h1>Ask your government.</h1><p>Text now. Voice, RAG and tool calling ready for backend integration.</p></div><span className="ai-live"><span/> AI READY</span></div>
      <div className="suggestions">{["Meri complaint ka status batao", "Mere district ke officers dikhao", "Pending complaints kitni hain?", "Revenue department ke services kya hain?"].map(x => <button key={x} onClick={() => setInput(x)}><Sparkles size={14}/>{x}</button>)}</div>
      <Card className="chat-card"><div className="messages">{messages.map((m,i) => <div className={`message ${m.role}`} key={i}><div className="message-icon">{m.role === "ai" ? <Bot size={17}/> : <UserRound size={17}/>}</div><div><span>{m.role === "ai" ? "UP_AI" : "You"}</span><p>{m.text}</p>{m.role === "ai" && i > 0 && <div className="source-chip">Sources will appear here after RAG integration</div>}</div></div>)}</div><div className="chat-input"><button className="voice-button" aria-label="Voice assistant"><Mic size={19}/></button><Input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter" && send()} placeholder="Ask anything about UP services..." /><Button onClick={send}><Send size={18}/></Button></div></Card>
    </div>
  </div>;
}