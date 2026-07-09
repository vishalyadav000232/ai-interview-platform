import { create } from "zustand";

import type { AuthState } from "../types/auth";



export const useAuthStore = create<AuthState>((set) => ({
    
    user: null,

    isAuthenticated: false,

    isLoading: true,

    setUser: (user) =>
        set({
            user,
            isAuthenticated: true,
        }),

    clearUser: () =>
        set({
            user: null,
            isAuthenticated: false,
        }),

    setLoading: (loading) =>
        set({
            isLoading: loading,
        }),
}));
