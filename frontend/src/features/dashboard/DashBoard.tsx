import { LogoutButton } from "../auth/components/common/LogoutButton";
import { useAuthStore } from "../auth/store/auth.store";

export const DashBoard = () => {
  const user = useAuthStore((state) => state.user);

  const isAuthenticated = useAuthStore(
    (state) => state.isAuthenticated
  );

  console.log("User from auth store:", user);
  console.log("Is authenticated:", isAuthenticated);

  return (
    <div>
      <h1>AI Interview Platform</h1>
      <LogoutButton/>

      {isAuthenticated && user ? (
        <div>
          <h2>Welcome, {user.first_name}</h2>
          <p>{user.email}</p>
        </div>
      ) : (
        <p>User is not authenticated</p>
      )}
    </div>
  );
};
