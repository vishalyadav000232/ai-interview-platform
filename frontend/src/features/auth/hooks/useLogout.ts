import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { useAuthStore } from "../store/auth.store"
import { logoutUser } from "../api/auth"
import { clearAccessToken } from "../../../api/auth_token"
import { notify } from "../../../shared/lib/toast"



export const useLogout = ()=>{


    const navigate = useNavigate()
    const queryClinet = useQueryClient()

    const clearUser = useAuthStore(state=>state?.clearUser)

    return useMutation({

        mutationKey : ["logout"] ,
        mutationFn : logoutUser,

        onSuccess:(res)=>{
            if(res?.success){

                clearAccessToken()
                clearUser()
                queryClinet.clear()
                notify.success(res?.message)

                navigate("/login", {
                    replace: true,
                });


            }

        },


        onError:(error)=>{

            clearAccessToken()
            clearUser()
            queryClinet.clear()

            notify?.error(error?.message)


            navigate("/login" , {
                replace:true,
            })





        }

    })

}
