import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";

import { authQueries } from "../api/auth.query";
import { useAuthStore } from "../store/auth.store";
import {
    clearAccessToken,
    getAccessToken,
} from "../../../api/auth_token";

export const useCurrentUser = () => {
    const setUser = useAuthStore((state) => state.setUser);
    const clearUser = useAuthStore((state) => state.clearUser);
    const setLoading = useAuthStore((state) => state.setLoading);

    const hasAccessToken = Boolean(getAccessToken());

    const query = useQuery({
        ...authQueries.me(),
        enabled: hasAccessToken,
        retry: false,
    });

    useEffect(() => {
        if (!hasAccessToken) {
            clearUser();
            setLoading(false);
            return;
        }

        if (query.isSuccess && query.data) {
            console.log("from usegetCurrent " , query?.data)
            setUser(query?.data);
            setLoading(false);
            return;
        }

        if (query.isError) {
            clearAccessToken();
            clearUser();
            setLoading(false);
        }
    }, [
        hasAccessToken,
        query.isSuccess,
        query.isError,
        query.data,
        setUser,
        clearUser,
        setLoading,
    ]);

    return query;
};
