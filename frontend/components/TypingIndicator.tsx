export default function TypingIndicator() {
  return (
    <div className="flex w-full justify-start" aria-live="polite" aria-label="Assistant is typing">
      <div className="flex items-center gap-1.5 rounded-chat rounded-bl-sm border border-border bg-surface px-4 py-3">
        <span className="h-1.5 w-1.5 rounded-full bg-muted animate-dot1" />
        <span className="h-1.5 w-1.5 rounded-full bg-muted animate-dot2" />
        <span className="h-1.5 w-1.5 rounded-full bg-muted animate-dot3" />
      </div>
    </div>
  );
}
