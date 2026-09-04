type TagColor = {
	text: string;
	border: string;
	bg: string;
	dot: string;
	shadow: string;
};

const TAG_COLORS: Record<string, TagColor> = {
	exam: {
		shadow: "shadow-amber-500/50",
		text: "text-amber-400",
		border: "border-amber-500/40",
		bg: "bg-amber-500/10",
		dot: "bg-amber-400",
	},
	result: {
		shadow: "shadow-emerald-500/50",
		text: "text-emerald-400",
		border: "border-emerald-500/40",
		bg: "bg-emerald-500/10",
		dot: "bg-emerald-400",
	},
	form_fill_up: {
		shadow: "shadow-blue-500/50",
		text: "text-blue-400",
		border: "border-blue-500/40",
		bg: "bg-blue-500/10",
		dot: "bg-blue-400",
	},
	syllabus: {
		shadow: "shadow-purple-500/50",
		text: "text-purple-400",
		border: "border-purple-500/40",
		bg: "bg-purple-500/10",
		dot: "bg-purple-400",
	},
	admission: {
		shadow: "shadow-rose-500/50",
		text: "text-rose-400",
		border: "border-rose-500/40",
		bg: "bg-rose-500/10",
		dot: "bg-rose-400",
	},
	routine: {
		shadow: "shadow-cyan-500/50",
		text: "text-cyan-400",
		border: "border-cyan-500/40",
		bg: "bg-cyan-500/10",
		dot: "bg-cyan-400",
	},
};

const SEM_COLOR: TagColor = {
	shadow: "shadow-slate-500/50",
	text: "text-slate-400",
	border: "border-slate-500/40",
	bg: "bg-slate-500/10",
	dot: "bg-slate-400",
};

const DEFAULT_COLOR: TagColor = {
	shadow: "shadow-neutral-500/50",
	text: "text-neutral-400",
	border: "border-neutral-600/40",
	bg: "bg-neutral-600/10",
	dot: "bg-neutral-400",
};

export function getTagColor(tag: string): TagColor {
	if (TAG_COLORS[tag]) return TAG_COLORS[tag];
	if (tag.endsWith("_sem")) return SEM_COLOR;
	return DEFAULT_COLOR;
}
