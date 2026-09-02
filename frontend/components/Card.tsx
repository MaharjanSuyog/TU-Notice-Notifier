import type { Notice } from "@/types/notice";
import { isAfter, formatDistanceToNow, subDays, format } from "date-fns";

type CardProps = {
	notice: Notice;
};
export default function Card({ notice }: CardProps) {
	const noticeDate = new Date(notice.published_date);

	const isNoticeRecent: boolean = isAfter(noticeDate, subDays(new Date(), 2));

	const dateDisplay = isNoticeRecent
		? formatDistanceToNow(noticeDate, { addSuffix: true })
		: format(noticeDate, "MMM d, yyyy");

	return (
		<a
			href={notice.href}
			target="_blank"
			className="pb-3 flex gap-3 hover:translate-x-1.5 hover:-translate-y-1.5 transition-transform ">
			<div className="pl-1 pt-1.5">
				{isNoticeRecent ? (
					<span className="relative flex h-3 w-3">
						<span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-pulse/75"></span>
						<span className="relative inline-flex rounded-full h-3 w-3 bg-pulse"></span>
					</span>
				) : (
					<span className="inline-flex rounded-full h-3 w-3 bg-muted/30"></span>
				)}
			</div>
			<div>
				<span className="font-mono text-muted">{dateDisplay}</span>
				<h2>{notice.title}</h2>
			</div>
		</a>
	);
}
