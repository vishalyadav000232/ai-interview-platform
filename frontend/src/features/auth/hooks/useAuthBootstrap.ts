import { useEffect } from "react";

import {
    clearAccessToken,
    setAccessToken,
} from "../../../api/auth_token";


import { useAuthStore } from "../store/auth.store";
import { getCurrentUser, refreshAccessToken } from "../api/auth";
import { notify } from "../../../shared/lib/toast";
import axios from "axios";

export const useAuthBootstrap = () => {
    const setUser = useAuthStore((state) => state.setUser);
    const clearUser = useAuthStore((state) => state.clearUser);
    const setLoading = useAuthStore((state) => state.setLoading);

    useEffect(() => {
        const restoreSession = async () => {
            try {
                setLoading(true);

                const accessToken = await refreshAccessToken();

                setAccessToken(accessToken);

                const user = await getCurrentUser();

                setUser(user);
            } catch (error) {

                console.log(error)

                if (
                    axios.isAxiosError(error) &&
                    error.response?.status === 401
                ) {
                    return;
                }
                console.error("Session restore failed:", error);
                notify.warning("No active session")

                clearAccessToken();
                clearUser();
            } finally {
                setLoading(false);
            }
        };

        restoreSession();
    }, [setUser, clearUser, setLoading]);
};
