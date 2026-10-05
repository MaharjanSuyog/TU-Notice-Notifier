export type Notice = {
	notice_id: number;
	published_date: string;
	title: string;
	href: string;
	tags: string[];
};

export type Tags = {
	program: string[];
	semester: string[];
	category: string[];
};
