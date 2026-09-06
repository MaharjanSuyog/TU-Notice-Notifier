"use client";

import { useAuth } from "@/utils/AuthContext";
import { Check } from "lucide-react";

export default function LoginButton() {
	const { user, loading, logout } = useAuth();

	if (loading) {
		return (
			<div className="text-slate-500 text-xs font-mono">
				Checking Session............
			</div>
		);
	}

	if (user) {
		return (
			<div className="flex items-center gap-3 text-sm font-mono text-slate-300">
				<span className="flex items-center gap-1.5 text-emerald-500">
					<Check size={13} /> {user.email}
				</span>

				<button
					onClick={logout}
					className="text-slate-500 hover:text-slate-300 underline">
					Sign Out
				</button>
			</div>
		);
	}

	return (
		<a
			href="/api/auth/google/login"
			className="bg-slate-800 hover:bg-slate-700 text-slate-100 text-sm font-mono px-3 py-2 rounded">
			Sign in with Google
		</a>
	);
}
