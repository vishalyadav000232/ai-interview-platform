import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

import { loginUser } from "../api/auth";
import { setAccessToken } from "../../../api/auth_token";
import { notify } from "../../../shared/lib/toast";
import { useAuthStore } from "../store/auth.store";



export const useLogin = () => {
    const navigate = useNavigate();

    const setUser = useAuthStore((state) => state.setUser);
    const setLoading = useAuthStore((state) => state.setLoading);

    return useMutation({
        mutationKey: ["login"],
        mutationFn: loginUser,
        retry: false,

        onSuccess: (response) => {
            if (!response?.success) {
                notify.error(response?.message || "Login failed");
                return;
            }

            const accessToken =
                response?.data?.access_token || response?.access_token;

            const user = response?.data?.user;

            console.log("login user" , user)
            console.log("LOGIN ACCEESS TOKEN",accessToken)


            if (!accessToken || !user) {
                notify.error("Invalid login response");
                return;
            }

            console.log(accessToken)

            setAccessToken(accessToken);
            setUser(user);
            setLoading(false);



            notify.success(response.message);

            navigate("/dashboard", {
                replace: true,
            });
        },

        onError: (error) => {
            console.error("Login failed:", error);

            if (axios.isAxiosError(error) && error?.response?.status == 401){
                return
            }

            notify.error(error?.message)       },
    });
};
