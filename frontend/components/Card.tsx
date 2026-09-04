import type { Notice } from "@/types/notice";
import { isAfter, formatDistanceToNow, subDays, format } from "date-fns";
import TagBadge from "@/components/TagBadge";
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
			rel="noopener noreferrer"
			className="pb-3 flex items-start gap-3 hover:translate-x-1.5 hover:-translate-y-1 transition-transform ">
			<div className="flex h-6 items-center shrink-0 mt-0.5">
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
				<div className="flex gap-5">
					<span className="font-mono text-muted flex items-center justify-center">
						{dateDisplay}
					</span>
					<div className="flex gap-2">
						{notice.tags.map((tag, i) => (
							<TagBadge key={i} tag={tag} />
						))}
					</div>
				</div>
				<h2>{notice.title}</h2>
			</div>
		</a>
	);
}
