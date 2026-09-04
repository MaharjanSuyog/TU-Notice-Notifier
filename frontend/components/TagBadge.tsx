import { getTagColor } from "@/utils/tagColors";

export default function TagBadge({ tag }: { tag: string }) {
	const c = getTagColor(tag);
	return (
		<span
			className={`font-mono uppercase border px-3 py-0.5 text-[10px] rounded-2xl flex justify-center items-center
								  transition-colors tracking-wide ${c.text} ${c.border} ${c.bg} `}>
			{tag.split("_").join(" ")}
		</span>
	);
}
