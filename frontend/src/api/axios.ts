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

        console.log(error?.config)

        if (!error.response) {
            notify.error("Network error. Please check your internet.");
            return Promise.reject(error);
        }

        const requestUrl = originalRequest?.url ?? ""



        const status = error.response.status;

        const isRefreshRequest =
            requestUrl.includes("/auth/refresh");

        if (status === 401 && isRefreshRequest) {
            clearAccessToken();

            return Promise.reject(error);
        }

        if (
            status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            !requestUrl.includes("/auth/refresh")&&
            !requestUrl.includes("/auth/login")&&
            !requestUrl.includes("/auth/register")

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
