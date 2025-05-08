import Login from "../pages/Login.tsx";
import ForgotPassword from "../pages/ForgotPassword.tsx";
import Dashboard from "../pages/Dashboard.tsx";
import Cars from "../pages/Cars.tsx";
import Rentals from "../pages/Rentals.tsx";
import Profile from "../pages/Profile.tsx";
export const routes = [
    {
        path: "login",
        component: <Login/>,
        isPrivate: false
    },
    {
        path: "forgot",
        component: <ForgotPassword/>,
        isPrivate: false
    },
    {
        path: "dashboard",
        component: <Dashboard/>,
        isPrivate: true
    },
    {
        path: "cars",
        component: <Cars/>,
        isPrivate: true
    },
    {
        path: "rentals",
        component: <Rentals/>,
        isPrivate: true
    },
    {
        path: "profile",
        component: <Profile/>,
        isPrivate: true
    },
]