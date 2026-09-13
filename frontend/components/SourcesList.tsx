import type { Source } from "@/lib/types";

interface Props {
  sources: Source[];
}

export default function SourcesList({ sources }: Props) {
  // De-duplicate by title — the same doc section can be retrieved more than once.
  const uniqueTitles = Array.from(new Set(sources.map((s) => s.title)));

  return (
    <div className="flex flex-wrap gap-1.5 px-1">
      {uniqueTitles.map((title) => (
        <span
          key={title}
          className="rounded-full border border-border bg-accent-soft px-2.5 py-0.5 text-xs font-medium text-accent"
        >
          {title}
        </span>
      ))}
    </div>
  );
}
