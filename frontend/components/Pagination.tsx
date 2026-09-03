"use client";

type PaginationProps = {
	page: number;
	totalPages: number;
	onPageChange: (page: number) => void;
};

export default function Pagination({
	page,
	totalPages,
	onPageChange,
}: PaginationProps) {
	return (
		<div className="flex items-center justify-center gap-4 font-mono text-sm ">
			<button
				disabled={page === 1}
				onClick={() => onPageChange(page - 1)}
				aria-label="Previous Page"
				className="w-8 h-8 flex items-center justify-center rounded border border-muted/40 cursor-pointer
                text-muted hover:border-muted hover:text-foreground transition-colors
                disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:border-muted/40 disabled:hover:text-muted">
				{"<"}
			</button>
			<span className="text-muted tabular-nums">
				Page {page} / {totalPages}
			</span>
			<button
				disabled={page === totalPages}
				onClick={() => onPageChange(page + 1)}
				aria-label="Next page"
				className="w-8 h-8 flex items-center justify-center rounded border border-muted/40 cursor-pointer
					text-muted hover:border-muted hover:text-foreground transition-colors
					disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:border-muted/40 disabled:hover:text-muted">
				{">"}
			</button>
		</div>
	);
}
