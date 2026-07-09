import { baseAPI } from "../../../api/axios"
import type { AuthResponse, AuthUser, LoginPayload, RegisterPayload } from "../types/auth"


export const loginUser = async (payload : LoginPayload) : Promise<AuthResponse> =>{
    const formData = new URLSearchParams();

    formData.append("username", payload.email);
    formData.append("password", payload.password);


    const response = await baseAPI.post("/auth/login" , formData , {
        headers:{
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    return response?.data
}



export const registerUser = async (
    payload: RegisterPayload,
): Promise<AuthResponse> => {
    const response = await baseAPI.post<AuthResponse>("/auth/register", payload)

    return response.data
}



export const getCurrentUser = async ():Promise<AuthUser>=>{

    const res = await baseAPI.get("/auth/me")

    return res?.data?.user
}

export const logoutUser = async (): Promise<void> => {
    await baseAPI.post("/auth/logout")
}
