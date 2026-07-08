import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios"
import { env } from "../config/env"
import { clearAccessToken, getAccessToken, setAccessToken } from "./auth_token"




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


baseAPI.interceptors.response.use(
    (response) => response,

    async (error: AxiosError) => {
        const originalRequest = error.config as RetryAxiosRequestConfig

        if (!error.response) {
            return Promise.reject(error)
        }

        const status = error.response.status

        if (
            status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            !originalRequest.url?.includes("/auth/refresh")
        ) {
            originalRequest._retry = true

            try {
                const refreshResponse = await baseAPI.post<RefreshResponse>(
                    "/auth/refresh",
                )

                const newAccessToken = refreshResponse?.data?.data?.access_token

                setAccessToken(newAccessToken)

                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

                return baseAPI(originalRequest)
            } catch (refreshError) {
                clearAccessToken()

                window.location.href = "/login"

                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    },
)
