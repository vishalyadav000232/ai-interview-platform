import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from "react-router-dom";

import { AppLayout } from "../components/layout/AppLayout";

import LandingPage from "../pages/Landing/LandingPage";
import { LoginPage } from "../features/auth/page/Login/LoginPage";
import { RegisterPage } from "../features/auth/page/Register/RegisterPage";
import { DashboardPage } from "../features/dashboard/pages/DashboardPage";

import { ProtectedRoute } from "./ProtectedRoute";
import { ResumePage } from "../features/resume/pages/ResumePage";

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
        element: <AppLayout />,
        children: [
          {
            path: "/dashboard",
            element: <DashboardPage />,
          },
          {
            path: "resume",
            element: <ResumePage />,
          }
        ],
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/" replace />,
  },
]);

export default function AppRoutes() {
  return <RouterProvider router={router} />;
}
