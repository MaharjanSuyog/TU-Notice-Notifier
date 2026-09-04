"use client";

import { fetchTags } from "@/utils/api";
import { getTagColor } from "@/utils/tagColors";
import { useEffect, useState } from "react";

type Props = {
	activeTags: string[];
	onToggle: (tag: string) => void;
	onClear: () => void;
};

export default function TagFilter({ activeTags, onToggle, onClear }: Props) {
	const [tags, setTags] = useState<string[]>([]);

	useEffect(() => {
		const controller = new AbortController();
		fetchTags(controller.signal)
			.then((data) => setTags(data.tags))
			.catch((err) => {
				console.log(err);
				setTags([]);
			});
		return () => controller.abort();
	}, []);

	const isClearActive = activeTags.length === 0;

	return (
		<div className="flex flex-wrap gap-2 font-mono text-xs uppercase tracking-wide">
			<button
				onClick={onClear}
				className={`flex items-center gap-1.5 rounded-sm border px-2.5 py-1 transition-colors ${
					isClearActive
						? "border-foreground/40 text-foreground"
						: "border-muted/30 text-muted hover:border-muted/60"
				}`}>
				<span
					className={`h-1.5 w-1.5 rounded-full bg-foreground transition-opacity ${
						isClearActive ? "opacity-100" : "opacity-0"
					}`}
				/>
				all
			</button>

			{tags.map((tag) => {
				const active = activeTags.includes(tag);
				const c = getTagColor(tag);

				return (
					<button
						key={tag}
						onClick={() => onToggle(tag)}
						className={`flex items-center gap-1.5 rounded-sm border px-2.5 py-1 uppercase transition-colors  cursor-pointer ${
							active
								? `${c.border} ${c.text} ${c.bg} ${c.shadow} shadow-2xs hover:-translate-y-1.5 hover:translate-x-1.5`
								: "border-muted/30 text-muted hover:border-muted/60 "
						}`}>
						<span
							className={`h-1.5 w-1.5 rounded-full ${c.dot} transition-opacity ${
								active ? "opacity-100" : "opacity-0"
							}`}
						/>
						{tag.split("_").join(" ")}
					</button>
				);
			})}
		</div>
	);
}
