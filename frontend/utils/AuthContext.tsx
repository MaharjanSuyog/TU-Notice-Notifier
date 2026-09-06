"use client";

import {
	createContext,
	ReactNode,
	useContext,
	useEffect,
	useState,
} from "react";

interface User {
	email: string;
	status: "active" | "unsubscribed";
	is_admin: boolean;
}

interface AuthContextValue {
	user: User | null;
	loading: boolean;
	logout: () => Promise<void>;
	refreshSession: () => Promise<void>;
}
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
	const [user, setUser] = useState<User | null>(null);
	const [loading, setLoading] = useState(true);

	const refreshSession = async () => {
		try {
			const res = await fetch(`/api/auth/me`, {
				credentials: "include",
			});
			setUser(res.ok ? await res.json() : null);
		} catch {
			setUser(null);
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		// eslint-disable-next-line react-hooks/set-state-in-effect
		refreshSession();
	}, []);

	const logout = async () => {
		await fetch(`/api/auth/logout`, {
			method: "POST",
			credentials: "include",
		});

		setUser(null);
	};

	return (
		<AuthContext.Provider value={{ user, logout, loading, refreshSession }}>
			{children}
		</AuthContext.Provider>
	);
}

export function useAuth(): AuthContextValue {
	const ctx = useContext(AuthContext);
	if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
	return ctx;
}
