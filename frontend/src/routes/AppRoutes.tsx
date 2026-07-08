import {createBrowserRouter , RouterProvider} from "react-router-dom";

import { LoginPage } from "../pages/Login/LoginPage";
import { RegisterPage } from "../pages/Register/RegisterPage";
import LandingPage from "../pages/Landing/LandingPage";



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