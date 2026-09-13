import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Neutral base — clean, minimal, not the default AI-slop palette.
        canvas: "#FAFAFA",
        surface: "#FFFFFF",
        border: "#E4E4E7",
        ink: "#18181B",
        muted: "#71717A",
        // Single accent, used sparingly (user bubble + send button + focus ring).
        accent: {
          DEFAULT: "#3B5BFD",
          hover: "#2E48D8",
          soft: "#EEF1FF",
        },
        danger: "#DC2626",
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "sans-serif",
        ],
      },
      borderRadius: {
        chat: "1rem",
      },
      maxWidth: {
        chat: "48rem",
      },
      keyframes: {
        dot: {
          "0%, 80%, 100%": { opacity: "0.25" },
          "40%": { opacity: "1" },
        },
      },
      animation: {
        dot1: "dot 1.2s infinite ease-in-out",
        dot2: "dot 1.2s infinite ease-in-out 0.2s",
        dot3: "dot 1.2s infinite ease-in-out 0.4s",
      },
    },
  },
  plugins: [],
};

export default config;
