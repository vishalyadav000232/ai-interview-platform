import { useMutation } from "@tanstack/react-query"
import { loginUser } from "../api/auth"
import { setAccessToken } from "../../../api/auth_token"
import { notify } from "../../../shared/lib/toast"
import { useNavigate } from "react-router-dom"

export const useLogin = () => {
    const navigation = useNavigate()
    return useMutation({
        mutationKey: ["login"],
        mutationFn: loginUser,
        retry: false,

        onSuccess: (response) => {

            if(response?.success){
                const accessToken = response?.data?.access_token

                notify.success(response?.message)
                navigation("/dashboard")



                if (accessToken) {
                    setAccessToken(accessToken)
                }
            }

        },

        onError: (error) => {
            console.error("Login failed:", error)
        },
    })
}
