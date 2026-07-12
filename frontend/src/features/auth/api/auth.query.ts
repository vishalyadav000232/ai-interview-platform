import { queryOptions } from "@tanstack/react-query"
import { getCurrentUser } from "./auth"


export const authKeys = {

    all : ["auth"] as const ,
    me : ()=> [...authKeys.all , "me"] as const

}



export const authQueries = {
    me : ()=> queryOptions(
        {
            queryKey:authKeys.me(),
            queryFn : getCurrentUser,
            staleTime: 1000 * 60* 10
        }
    )
}


