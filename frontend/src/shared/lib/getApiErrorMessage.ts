import axios from "axios";

type ApiErrorResponse = {
    message?: string;
    detail?: string;
};

export const getApiErrorMessage = (
    error: unknown,
    fallback = "Something went wrong"
): string => {
    if (!axios.isAxiosError<ApiErrorResponse>(error)) {
        return fallback;
    }

    return (
        error.response?.data?.message ||
        error.response?.data?.detail ||
        fallback
    );
};
