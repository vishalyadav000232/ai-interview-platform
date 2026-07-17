import { useEffect } from "react";
import axios from "axios";

import {
    clearAccessToken,
    setAccessToken,
} from "../../../api/auth_token";

import { getCurrentUser, refreshAccessToken } from "../api/auth";
import { useAuthStore } from "../store/auth.store";
import { notify } from "../../../shared/lib/toast";

export const useAuthBootstrap = () => {
    const setUser = useAuthStore((state) => state.setUser);
    const clearUser = useAuthStore((state) => state.clearUser);
    const setLoading = useAuthStore((state) => state.setLoading);

    useEffect(() => {
        let isMounted = true;

        const restoreSession = async () => {
            setLoading(true);

            try {
                const accessToken = await refreshAccessToken();

                if (!isMounted) {
                    return;
                }

                setAccessToken(accessToken);

                const user = await getCurrentUser();

                if (!isMounted) {
                    return;
                }

                setUser(user);
            } catch (error) {
                if (!isMounted) {
                    return;
                }

                clearAccessToken();
                clearUser();

                const isUnauthorized =
                    axios.isAxiosError(error) &&
                    error.response?.status === 401;

                if (!isUnauthorized) {
                    console.error("Session restore failed:", error);
                    notify.error("Unable to restore your session");
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };

        void restoreSession();

        return () => {
            isMounted = false;
        };
    }, [setUser, clearUser, setLoading]);
};
