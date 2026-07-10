import type { PropsWithChildren } from "react";
import { useCurrentUser } from "../features/auth/hooks/useCurrentUser";




export function AuthProvider({children}:PropsWithChildren){
    useCurrentUser()
    return children
}
