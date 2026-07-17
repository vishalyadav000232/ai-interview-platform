import {
    Navigate,
    Outlet,
    useLocation,
} from "react-router-dom";

import { useAuthStore } from "../features/auth/store/auth.store";

export function ProtectedRoute() {
    const location = useLocation();

    const isAuthenticated = useAuthStore(
        (state) => state.isAuthenticated,
    );

    const isLoading = useAuthStore(
        (state) => state.isLoading,
    );

    if (isLoading) {
        return (
            <main
                className="min-h-screen flex items-center justify-center bg-slate-950"
                aria-busy="true"
                aria-live="polite"
            >
                <div className="flex flex-col items-center gap-4">
                    <div
                        className="h-10 w-10 animate-spin rounded-full border-4 border-slate-700 border-t-violet-500"
                        aria-hidden="true"
                    />

                    <p className="text-sm text-slate-400">
                        Preparing your workspace...
                    </p>
                </div>
            </main>
        );
    }

    if (!isAuthenticated) {
        return (
            <Navigate
                to="/login"
                replace
                state={{
                    from: `${location.pathname}${location.search}${location.hash}`,
                }}
            />
        );
    }

    return <Outlet />;
}
