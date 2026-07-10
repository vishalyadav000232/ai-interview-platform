import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios"
import { env } from "../config/env"
import { clearAccessToken, getAccessToken, setAccessToken } from "./auth_token"
import { notify } from "../shared/lib/toast"




export const baseAPI = axios.create({
    baseURL: env.API_BASE_URL,
    withCredentials: true,
    timeout: 10000,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
    }
})


baseAPI.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const token = getAccessToken()
        console.log("this is the token from the " , token)

        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config

    },
    (error) => {
        return Promise.reject(error)
    }
)

type DataResponse = {
    access_token : string,
    token_type : string
}


type RefreshResponse = {
    success : boolean,
    message : string,
    data: DataResponse
}

type RetryAxiosRequestConfig = InternalAxiosRequestConfig & {
    _retry?: boolean
}

type ApiErrorResponse = {
    message?: string;
    detail?: string;
};

baseAPI.interceptors.response.use(
    (response) => response,

    async (error: AxiosError<ApiErrorResponse>) => {
        const originalRequest = error.config as RetryAxiosRequestConfig;

        if (!error.response) {
            notify.error("Network error. Please check your internet.");
            return Promise.reject(error);
        }

        const status = error.response.status;

        if (
            status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            !originalRequest.url?.includes("/auth/refresh")&&
            !originalRequest.url?.includes("auth/login")&&
            !originalRequest.url?.includes("auth/register")

        ) {
            originalRequest._retry = true;

            try {
                const refreshResponse = await baseAPI.post<RefreshResponse>(
                    "/auth/refresh"
                );

                const newAccessToken =
                    refreshResponse.data?.data?.access_token;

                if (!newAccessToken) {
                    throw new Error("Access token missing");
                }

                setAccessToken(newAccessToken);

                originalRequest.headers = originalRequest.headers ?? {};
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                return baseAPI(originalRequest);
            } catch (refreshError) {
                clearAccessToken();
                window.location.href = "/login";

                return Promise.reject(refreshError);
            }
        }

        const message =
            error.response.data?.message ||
            error.response.data?.detail ||
            "Something went wrong";

        notify.error(message);

        return Promise.reject(error);
    }
);
