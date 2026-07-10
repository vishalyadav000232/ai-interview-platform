import { createBrowserRouter, RouterProvider } from "react-router-dom";

import LandingPage from "../pages/Landing/LandingPage";
import { LoginPage } from "../features/auth/page/Login/LoginPage";
import { RegisterPage } from "../features/auth/page/Register/RegisterPage";

import { ProtectedRoute } from "./ProtectedRoute";
import { DashBoard } from "../features/dashboard/DashBoard";


const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />,
  },

  {
    path: "/login",
    element: <LoginPage />,
  },

  {
    path: "/register",
    element: <RegisterPage />,
  },

  {
    element: <ProtectedRoute />,
    children: [
      {
        path: "/dashboard",
        element: <DashBoard />,
      },
    ],
  },
]);

export default function AppRoutes() {
  return <RouterProvider router={router} />;
}
