"use client";

import { useEffect, useRef, useState } from "react";
import type { ChatMessage, Source } from "@/lib/types";
import { ApiError, sendChatMessageStream  } from "@/lib/api";
import { getOrCreateSessionId, setSessionId } from "@/lib/session";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";

const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Hi! I'm the NovaSaaS support assistant. Ask me anything about billing, your account, or the product — I'll answer from our documentation.",
};

function makeId(): string {
  return crypto.randomUUID();
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [isSending, setIsSending] = useState(false);
  const [sessionId, setLocalSessionId] = useState<string | null>(null);
  const scrollAnchorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setLocalSessionId(getOrCreateSessionId());
  }, []);

  useEffect(() => {
    scrollAnchorRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);

  async function handleSend(text: string) {
    const userMessage: ChatMessage = { id: makeId(), role: "user", content: text };
    const assistantId = makeId();
  
    setMessages((prev) => [
      ...prev,
      userMessage,
      { id: assistantId, role: "assistant", content: "" },
    ]);
    setIsSending(true);
  
    try {
      await sendChatMessageStream(
        text,
        sessionId,
        (token) => {
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + token } : m))
          );
        },
        (newSessionId, sources) => {
          setSessionId(newSessionId);
          setLocalSessionId(newSessionId);
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, sources } : m))
          );
        }
      );
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
      setMessages((prev) =>
        prev.map((m) => (m.id === assistantId ? { ...m, content: message, failed: true } : m))
      );
    } finally {
      setIsSending(false);
    }
  }

  // Retries the most recent user message after a failure.
  function handleRetry() {
    const lastUser = [...messages].reverse().find((m) => m.role === "user");
    if (!lastUser) return;
    setMessages((prev) => prev.filter((m) => !m.failed));
    handleSend(lastUser.content);
  }

  return (
    <div className="flex h-dvh flex-col bg-canvas">
      <header className="border-b border-border bg-surface px-4 py-3.5 sm:px-6">
        <div className="mx-auto flex max-w-chat items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent-soft text-sm font-semibold text-accent">
            N
          </div>
          <div>
            <h1 className="text-sm font-semibold text-ink">NovaSaaS Support</h1>
            <p className="text-xs text-muted">Usually replies in a few seconds</p>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto px-4 py-4 sm:px-6">
        <div className="mx-auto flex max-w-chat flex-col gap-4">
          {messages.map((message) =>
            message.role === "assistant" && message.content === "" ? null : (
              <MessageBubble
                key={message.id}
                message={message}
                onRetry={message.failed ? handleRetry : undefined}
              />
            )
          )}
          {isSending &&
            messages[messages.length - 1]?.content === "" && <TypingIndicator />}
          <div ref={scrollAnchorRef} />
        </div>
      </div>

      <ChatInput onSend={handleSend} disabled={isSending} />
    </div>
  );
}
