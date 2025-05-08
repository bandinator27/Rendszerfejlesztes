import {useContext, useEffect} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import {emailKeyName, roleKeyName, tokenKeyName} from "../constants/constants.ts";
import api from "../api/api.ts";
import {jwtDecode} from "jwt-decode";

const useAuth = () => {
    const { token, setToken, email, setEmail, role, setRole  } = useContext(AuthContext);
    const isLoggedIn = !!token;

    const login = (email: string, password: string) => {
        api.Auth.login(email, password).then((res) => {
            setToken(res.data.token);
            localStorage.setItem(tokenKeyName, res.data.token);
            const decodedToken: never = jwtDecode(res.data.token);
            const role = decodedToken['roles'];
            setRole(role);
            localStorage.setItem(roleKeyName, role);
            setEmail(email);
            localStorage.setItem(emailKeyName, email);
        });
    }

    const logout = () => {
        localStorage.clear();
        setToken(null);
    }

    useEffect(() => {

    }, []);

    return {login, logout, token, email, isLoggedIn, role, setRole};
}

export default useAuth;