import type { Metadata } from "next";
import {
	Manrope,
	Caveat,
	Space_Mono,
	Plus_Jakarta_Sans,
} from "next/font/google";
import "./globals.css";

const manrope = Manrope({
	subsets: ["latin"],
	variable: "--font-manrope",
	weight: ["200", "300", "400", "500", "600", "700", "800"],
});
const pjs = Plus_Jakarta_Sans({
	subsets: ["latin"],
	variable: "--font-plus-jartika-sans",
	weight: ["200", "300", "400", "500", "600", "700", "800"],
});

const spaceMono = Space_Mono({
	subsets: ["latin"],
	variable: "--font-space-mono",
	weight: ["400", "700"],
});

const caveat = Caveat({
	subsets: ["latin"],
	variable: "--font-caveat",
	weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
	title: "TU Notice Notifier",
	description: "Get Notified and View New Notices from iost.tu.edu.np",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
	return (
		<html
			lang="en"
			className={`${manrope.variable} ${spaceMono.variable} ${caveat.variable} ${pjs.variable} h-full antialiased`}>
			<body className="min-h-full flex flex-col">{children}</body>
		</html>
	);
}
