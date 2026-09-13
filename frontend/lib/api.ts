import type { ChatResponse, Source } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status?: number;
  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Sends a message to the backend /chat endpoint.
 * Throws ApiError with a user-facing message on any failure.
 */
export async function sendChatMessage(
  message: string,
  sessionId: string | null
): Promise<ChatResponse> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
  } catch {
    throw new ApiError(
      "Can't reach the server. Check that the backend is running."
    );
  }

  if (!response.ok) {
    let detail = "Something went wrong. Please try again.";
    try {
      const body = await response.json();
      if (body?.detail) detail = body.detail;
    } catch {
      // response wasn't JSON — keep the default message
    }
    throw new ApiError(detail, response.status);
  }

  return response.json();
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    return res.ok;
  } catch {
    return false;
  }
}

export async function sendChatMessageStream(
  message: string,
  sessionId: string | null,
  onToken: (text: string) => void,
  onDone: (sessionId: string, sources: Source[]) => void
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  if (!response.ok || !response.body) {
    throw new ApiError("Can't reach the server. Check that the backend is running.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const events = buffer.split("\n\n");
    buffer = events.pop() ?? "";

    for (const event of events) {
      if (!event.startsWith("data: ")) continue;
      const payload = JSON.parse(event.slice(6));
      if (payload.type === "token") onToken(payload.text);
      else if (payload.type === "done") onDone(payload.session_id, payload.sources);
    }
  }
}