"use client";
import { useState, useEffect } from "react";
import Card from "@/components/Card";
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

	const pageSize = 10;

	const [noticeData, setNoticeData] = useState<NoticeResponse>({
		page: 1,
		notices: [],
		total: 0,
		page_size: pageSize,
		total_pages: 1,
	});

	useEffect(() => {
		async function fetchNotices() {
			try {
				setLoading(true);
				const response = await fetch(
					`/api/notices?page=${page}&page_size=${pageSize}`,
				);

				if (!response.ok) throw new Error("Failed to fetch notices");

				const data: NoticeResponse = await response.json();
				setNoticeData(data);
			} catch (err) {
				console.error("Error fetching notices: ", err);
			} finally {
				setLoading(false);
			}
		}

		fetchNotices();
	}, [page]);

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
					{loading ? (
						<p>Loading.... </p>
					) : (
						<>
							<div className="flex flex-col divide-y  divide-muted/30 gap-2">
								{noticeData?.notices.map((notice) => (
									<Card key={notice.notice_id} notice={notice} />
								))}
							</div>
							<div className="flex gap-3 ">
								<button
									disabled={page === 1}
									onClick={() => setPage((prev) => prev - 1)}>
									{"<"}
								</button>
								<span>
									{" "}
									Page {page} / {noticeData?.total_pages}{" "}
								</span>
								<button
									disabled={page === noticeData?.total_pages}
									onClick={() => setPage((prev) => prev + 1)}>
									{">"}
								</button>
							</div>
						</>
					)}
				</div>
			</main>
		</div>
	);
}
