"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useMemo, useCallback } from "react";

export function useNoticeFilters() {
	const router = useRouter();
	const pathname = usePathname();
	const searchParams = useSearchParams();

	const activeTags = useMemo(() => {
		const raw = searchParams.get("tags");
		return raw ? raw.split(",") : [];
	}, [searchParams]);

	const page = Number(searchParams.get("page") ?? "1");

	const updateParams = useCallback(
		(next: { tags?: string[]; page?: number }) => {
			const params = new URLSearchParams(searchParams.toString());

			if (next.tags !== undefined) {
				if (next.tags.length > 0) {
					params.set("tags", next.tags.join(","));
				} else {
					params.delete("tags");
					if (params.get("page")) params.delete("page");
				}
			}

			if (next.page !== undefined) {
				params.set("page", String(next.page));
			}

			router.push(`${pathname}?${params.toString()}`, { scroll: false });
		},
		[router, pathname, searchParams],
	);

	const toggleTag = useCallback(
		(tag: string) => {
			const next = activeTags.includes(tag)
				? activeTags.filter((t) => t !== tag)
				: [...activeTags, tag];
			updateParams({ tags: next });
		},
		[activeTags, updateParams],
	);

	const clearTags = useCallback(
		() => updateParams({ tags: [] }),
		[updateParams],
	);
	const setPage = useCallback(
		(p: number) => updateParams({ page: p }),
		[updateParams],
	);

	return { activeTags, page, toggleTag, clearTags, setPage };
}
