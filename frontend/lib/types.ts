export type ChatRole = "user" | "assistant";

export interface Source {
  id: string;
  title: string;
  distance: number;
}

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  sources?: Source[];
  /** Set on an assistant message that failed to load, so the UI can offer a retry. */
  failed?: boolean;
}

export interface ChatResponse {
  session_id: string;
  answer: string;
  sources: Source[];
}
