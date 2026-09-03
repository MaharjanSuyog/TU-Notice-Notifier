"use client";
import { useState, useEffect } from "react";
import Card from "@/components/Card";
import Pagination from "@/components/Pagination";
import type { Notice } from "@/types/notice";

type NoticeResponse = {
	page: number;
	page_size: number;
	total: number;
	total_pages: number;
	notices: Notice[];
};

export default function Home() {
	const [page, setPage] = useState(1);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	const pageSize = 10;

	const [noticeData, setNoticeData] = useState<NoticeResponse | null>(null);

	useEffect(() => {
		const controller = new AbortController();

		async function fetchNotices() {
			try {
				setLoading(true);
				setError(null);

				const response = await fetch(
					`/api/notices?page=${page}&page_size=${pageSize}`,
					{ signal: controller.signal },
				);

				if (!response.ok) throw new Error("Failed to fetch notices");

				const data: NoticeResponse = await response.json();
				setNoticeData(data);
			} catch (err) {
				if (err instanceof DOMException && err.name === "AbortError") return;
				console.error("Error fetching notices: ", err);
				setError("Couldn't load notices. Please try again.");
			} finally {
				setLoading(false);
			}
		}

		fetchNotices();
		return () => controller.abort();
	}, [page]);

	const handlePageChange = (newPage: number) => {
		setPage(newPage);
		window.scrollTo({ top: 0, behavior: "smooth" });
	};
	return (
		<div className="flex flex-col flex-1 items-center mt-20 font-sans dark:bg-slate min-h-screen">
			<main className="w-3/4 flex flex-col gap-10">
				<span>
					<h1 className="font-handwritten font-extrabold text-8xl ">
						RECENT NOTICES
					</h1>
					<span className="font-mono text-muted">watching: iost.tu.edu.np</span>
				</span>
				<div className="mb-10">
					{loading || noticeData === null ? (
						<p className="font-mono text-muted">Loading.... </p>
					) : error ? (
						<p className="font-mono text-error">{error}</p>
					) : noticeData.notices.length === 0 ? (
						<p className="font-mono text-muted">No notices found.</p>
					) : (
						<>
							{noticeData?.total_pages > 1 && (
								<Pagination
									page={page}
									totalPages={noticeData.total_pages}
									onPageChange={handlePageChange}
								/>
							)}
							<div className="flex flex-col divide-y divide-muted/30 gap-2">
								{noticeData.notices.map((notice) => (
									<Card key={notice.notice_id} notice={notice} />
								))}
							</div>
							{noticeData.total_pages > 1 && (
								<Pagination
									page={page}
									totalPages={noticeData.total_pages}
									onPageChange={handlePageChange}
								/>
							)}
						</>
					)}
				</div>
			</main>
		</div>
	);
}
