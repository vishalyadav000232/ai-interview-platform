import { useMutation } from "@tanstack/react-query";
import { registerUser } from "../api/auth";
import { notify } from "../../../shared/lib/toast";
import { getApiErrorMessage } from "../../../shared/lib/getApiErrorMessage";

export const useRegister = () => {
    return useMutation({
        mutationKey: ["register"],
        mutationFn: registerUser,
        retry: false,

        onSuccess: (response) => {
            notify.success(response?.message || "Registration successful");
        },

        onError: (error) => {
            const message = getApiErrorMessage(
                error,
                "Registration failed"
            );

            notify.error(message);
        },
    });
};
