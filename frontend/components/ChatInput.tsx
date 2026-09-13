"use client";

import { useRef, useState, type KeyboardEvent } from "react";

const MAX_LENGTH = 500;

interface Props {
  onSend: (message: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function handleSubmit() {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleInput(e: React.ChangeEvent<HTMLTextAreaElement>) {
    setValue(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 120)}px`;
  }

  const remaining = MAX_LENGTH - value.length;
  const nearLimit = remaining <= 40;

  return (
    <div className="border-t border-border bg-surface px-4 py-3 sm:px-6">
      <div className="mx-auto flex max-w-chat items-end gap-2">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          maxLength={MAX_LENGTH}
          rows={1}
          placeholder="Ask about NovaSaaS…"
          aria-label="Message"
          className="max-h-[120px] flex-1 resize-none rounded-chat border border-border bg-canvas px-4 py-2.5 text-[15px] leading-relaxed text-ink placeholder:text-muted focus:border-accent focus:outline-none disabled:opacity-60"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-40"
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="M4 12L20 4L14 20L11 13L4 12Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinejoin="round"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>
      {nearLimit && (
        <p className="mx-auto mt-1.5 max-w-chat text-right text-xs text-muted">
          {remaining} characters left
        </p>
      )}
    </div>
  );
}
