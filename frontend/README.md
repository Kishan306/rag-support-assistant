# NovaSaaS Support Chat — Frontend

A minimal, production-structured chat UI for the NovaSaaS RAG support
assistant. Built with Next.js (App Router) and TypeScript, styled with
Tailwind CSS.

## Structure

```
app/
  layout.tsx        Root layout, fonts, metadata
  page.tsx           Renders the chat window
  globals.css         Tailwind entry + base styles
components/
  ChatWindow.tsx      Owns conversation state, orchestrates sending/receiving
  MessageBubble.tsx   Renders one message (user or assistant), distinct styling
  ChatInput.tsx       Auto-growing textarea + send button
  SourcesList.tsx     Chips showing which docs an answer came from
  TypingIndicator.tsx Animated "..." shown while waiting for a reply
lib/
  api.ts              Fetch wrapper for the FastAPI backend
  session.ts          Persists a session id in localStorage
  types.ts            Shared TypeScript types
```

## Running locally (without Docker)

Requires Node.js 20+.

```bash
npm install
cp .env.local.example .env.local   # adjust API URL if needed
npm run dev
```

Visit http://localhost:3000. The backend must be running at the URL set in
`.env.local` (defaults to `http://localhost:8000`).

## Running with Docker

From the repo root, this is normally started together with the backend via
`docker-compose up --build`. To run the frontend image standalone:

```bash
docker build -t novasaas-chat-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 novasaas-chat-frontend
```

## Notes on design choices

- **Single accent color**, used only for the user's messages and the send
  button — everything else stays neutral so the accent stays meaningful.
- **User and assistant messages are visually distinct**: user messages are
  right-aligned, solid accent-colored bubbles; assistant messages are
  left-aligned, bordered, near-white bubbles.
- **Session id** is generated client-side and stored in `localStorage`, so a
  page refresh continues the same conversation on the backend (which keeps
  short-term history per session).
- **Failure handling**: a failed request renders as a distinct red-tinted
  assistant bubble with a "Retry" action, rather than a browser alert or a
  silently dropped message.
- Fully responsive from narrow mobile widths up to desktop; layout uses a
  capped content width (`max-w-chat`) centered on larger screens.
