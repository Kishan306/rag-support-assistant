import type { ChatMessage } from "@/lib/types";
import SourcesList from "./SourcesList";

interface Props {
  message: ChatMessage;
  onRetry?: () => void;
}

export default function MessageBubble({ message, onRetry }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`flex max-w-[85%] flex-col gap-1.5 sm:max-w-[75%] ${
          isUser ? "items-end" : "items-start"
        }`}
      >
        <div
          className={[
            "rounded-chat px-4 py-2.5 text-[15px] leading-relaxed whitespace-pre-wrap break-words",
            isUser
              ? "bg-accent text-white rounded-br-sm"
              : message.failed
              ? "bg-red-50 text-danger border border-red-200 rounded-bl-sm"
              : "bg-surface text-ink border border-border rounded-bl-sm",
          ].join(" ")}
        >
          {message.content}
        </div>

        {message.failed && onRetry && (
          <button
            onClick={onRetry}
            className="text-xs font-medium text-accent hover:text-accent-hover transition-colors"
          >
            Retry
          </button>
        )}

        {!isUser && !message.failed && message.sources && message.sources.length > 0 && (
          <SourcesList sources={message.sources} />
        )}
      </div>
    </div>
  );
}
