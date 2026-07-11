import { useLogout } from "../../hooks/useLogout";


export const LogoutButton = () => {
    const logoutMutation = useLogout();

    const handleLogout = () => {
        logoutMutation.mutate();
    };

    return (
        <button
            type="button"
            onClick={handleLogout}
            disabled={logoutMutation.isPending}
        >
            {logoutMutation.isPending
                ? "Logging out..."
                : "Logout"}
        </button>
    );
};
