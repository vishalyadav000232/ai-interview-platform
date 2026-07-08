import {createBrowserRouter , RouterProvider} from "react-router-dom";

import LandingPage from "../pages/Landing/LandingPage";
import { LoginPage } from "../features/auth/page/Login/LoginPage";
import { RegisterPage } from "../features/auth/page/Register/RegisterPage";



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
]);

function AppRoutes(){
    return <RouterProvider router={router}>

    </RouterProvider>
}


export default AppRoutes;
