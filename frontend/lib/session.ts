const SESSION_KEY = "novasaas_chat_session_id";

/**
 * Returns the current chat session id, creating and persisting a new one
 * on first visit. Kept in localStorage so a page refresh continues the
 * same conversation on the backend.
 */
export function getOrCreateSessionId(): string {
  if (typeof window === "undefined") return "";

  const existing = window.localStorage.getItem(SESSION_KEY);
  if (existing) return existing;

  const fresh = crypto.randomUUID();
  window.localStorage.setItem(SESSION_KEY, fresh);
  return fresh;
}

export function setSessionId(id: string): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(SESSION_KEY, id);
}

export function clearSessionId(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(SESSION_KEY);
}
