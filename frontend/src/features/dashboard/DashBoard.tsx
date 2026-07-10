import { useAuthStore } from "../auth/store/auth.store"


export const DashBoard = () => {
    const {user} = useAuthStore(state=>state?.user)
    const {isAuthebtcated} = useAuthStore(state=>state?.isAuthenticated)

    console.log("tiis is the user from the auth store" , user)
    console.log(isAuthebtcated)
  return (
    <div>{isAuthebtcated}</div>
  )
}
