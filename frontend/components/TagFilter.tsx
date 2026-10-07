"use client";

import { fetchTags } from "@/utils/api";
import { getTagColor } from "@/utils/tagColors";
import { useEffect, useState } from "react";
import { Tags } from "@/types/notice";
type Props = {
	activeTags: string[];
	onChange: (tags: string[]) => void;
};

const EMPTY_TAGS: Tags = {
	program: [],
	semester: [],
	category: [],
};

const TAG_ORDER: (keyof Tags)[] = ["program", "semester", "category"];

function formatTag(tag: string, kind: string) {
	const clean = kind === "semester" ? tag.replace("_sem", "") : tag;
	return clean.replaceAll("_", " ");
}

export default function TagFilter({ activeTags, onChange }: Props) {
	const [tags, setTags] = useState<Tags>(EMPTY_TAGS);

	useEffect(() => {
		const controller = new AbortController();
		fetchTags(controller.signal)
			.then((data) => setTags(data.tags))
			.catch((err) => {
				if (err.name != "AbortError") {
					console.error("Failed to fetch tags: ", err);
					setTags(EMPTY_TAGS);
				}
			});
		return () => controller.abort();
	}, []);

	const isClearActive = activeTags.length === 0;

	const handleSelect = (kind: keyof Tags, tag: string) => {
		const rest = activeTags.filter((t) => !tags[kind].includes(t));
		onChange(activeTags.includes(tag) ? rest : [...rest, tag]);
	};
	return (
		<div className="space-y-3 font-mono text-xs uppercase tracking-wide">
			<button
				onClick={() => {
					if (!isClearActive) onChange([]);
				}}
				className={`group select-none flex cursor-pointer items-center gap-1.5 rounded-sm border px-2.5 py-1 transition-colors ${
					isClearActive
						? "border-foreground/40 text-foreground"
						: "border-muted/30 text-muted hover:border-muted/50 hover:text-foreground"
				}`}>
				<span
					className={`h-1.5 w-1.5 rounded-full bg-foreground transition-opacity ${
						isClearActive ? "opacity-100" : "opacity-0 group-hover:opacity-40"
					}`}
				/>
				all
			</button>
			{TAG_ORDER.map((kind) => {
				const categoryTags = tags[kind];
				if (categoryTags.length === 0) return null;
				return (
					<div
						key={kind}
						className="flex items-start md:items-center-safe gap-x-3 gap-y-2">
						<div className="flex w-20 shrink-0 items-center gap-2">
							<p className="font-mono text-xs uppercase tracking-widest text-muted/60">
								{" "}
								{kind}
							</p>
						</div>
						<div
							role="radiogroup"
							aria-label={kind}
							className="flex  flex-wrap gap-1.5 font-mono text-xs uppercase tracking-wide">
							{categoryTags.map((tag) => {
								const active = activeTags.includes(tag);
								const c = getTagColor(tag);
								return (
									<button
										key={tag}
										type="button"
										aria-pressed={active}
										onClick={() => handleSelect(kind, tag)}
										className={`group flex items-center gap-1.5 rounded-sm border px-2.5 py-1 uppercase transition-all  cursor-pointer ${
											active
												? `${c.border} ${c.text} ${c.bg} ${c.shadow} shadow-2xs hover:-translate-y-0.5 hover:translate-x-0.5`
												: "border-muted/30 text-muted hover:border-muted/60 "
										}`}>
										<span
											className={`h-1.5 w-1.5 rounded-full ${c.dot} transition-opacity ${
												active
													? "opacity-100"
													: "opacity-0 group-hover:opacity-40"
											}`}
										/>
										{formatTag(tag, kind)}
									</button>
								);
							})}
						</div>
					</div>
				);
			})}
		</div>
	);
}
