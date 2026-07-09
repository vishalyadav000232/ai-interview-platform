import { useMutation } from "@tanstack/react-query"
import { registerUser } from "../api/auth"
import { notify } from "../../../shared/lib/toast"









export const useRegister = ()=>{
    return useMutation({
        mutationKey : ["register"],
        mutationFn: registerUser,
        retry : false,

        onSuccess : (response)=>{

            notify.success(response?.message)
        },

        onError:(error)=>{
            notify.error(error?.message)
        }
        
    })
}
