import type { Metadata } from "next";
import {
	Manrope,
	Space_Mono,
	Plus_Jakarta_Sans,
	Nerko_One,
} from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/utils/AuthContext";
import Footer from "@/components/Footer";

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

const Nerko = Nerko_One({
	subsets: ["latin"],
	variable: "--font-nerko-one",
	weight: ["400"],
});
const spaceMono = Space_Mono({
	subsets: ["latin"],
	variable: "--font-space-mono",
	weight: ["400", "700"],
});

export const metadata: Metadata = {
	title: "TU Notice Notifier",
	description: "Get Notified and View New Notices from iost.tu.edu.np",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
	return (
		<html
			lang="en"
			className={`${manrope.variable} ${Nerko.variable} ${spaceMono.variable}  ${pjs.variable} h-full antialiased`}>
			<body className="min-h-full flex flex-col">
				<AuthProvider>
					<main className="flex-1">{children}</main>
					<Footer />
				</AuthProvider>
			</body>
		</html>
	);
}
