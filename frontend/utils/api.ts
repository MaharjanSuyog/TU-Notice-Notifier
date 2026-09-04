import type { Notice } from "@/types/notice";

export type NoticeResponse = {
	page: number;
	page_size: number;
	total: number;
	total_pages: number;
	notices: Notice[];
};

export type TagResponse = {
	tags: string[];
};
export async function fetchNotices(
	params: { page: number; pageSize: number; tags?: string[] },
	signal?: AbortSignal,
): Promise<NoticeResponse> {
	const query = new URLSearchParams();
	query.set("page", String(params.page));
	query.set("page_size", String(params.pageSize));

	if (params.tags && params.tags.length == 1) {
		query.set("tag", params.tags[0]);
	} else if (params.tags && params.tags.length > 1) {
		query.set("tags", params.tags.join(","));
	}

	const response = await fetch(`/api/notices?${query.toString()}`, { signal });

	if (!response.ok) throw new Error("Failed to fetch notices");
	return response.json();
}

export async function fetchTags(signal?: AbortSignal): Promise<TagResponse> {
	const response = await fetch(`/api/tags`, { signal });

	if (!response.ok) throw new Error("Failed to fetch tags");

	return response.json();
}
