import { baseAPI } from "../../../api/axios"
import type { LoginResponse, AuthUser, LoginPayload, RegisterPayload  , RegisterResponse} from "../types/auth"


export const loginUser = async (payload : LoginPayload) : Promise<LoginResponse> =>{
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
): Promise<RegisterResponse> => {
    const response = await baseAPI.post<RegisterResponse>("/auth/register", payload)

    return response.data
}



export const getCurrentUser = async ():Promise<AuthUser>=>{

    const res = await baseAPI.get("/auth/me")

    return res?.data?.user
}

export const logoutUser = async (): Promise<void> => {
    await baseAPI.post("/auth/logout")
}
