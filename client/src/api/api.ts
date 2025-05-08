import axiosInstance from "./axios.config.ts";
import {ICars} from "../interfaces/ICars.ts";
import {IRentals} from "../interfaces/IRentals.ts";
import {IProfile} from "../interfaces/IProfile.ts";

const Auth = {
    login: (email: string, password: string) => axiosInstance.post<{token: string}>(`/api/user/login`, {email, password})
}

const Cars = {
    getCars: () => axiosInstance.get<ICars[]>(`/api/car/view_cars`),
    getCar: (id: number) => axiosInstance.get<ICars>(`/api/car/${id}`),
}

const Rentals = {
    getRentals: () => axiosInstance.get<IRentals[]>(`/api/rental/view_rentals`),
    getRental: (id: number) => axiosInstance.get<IRentals>(`/api/rental/${id}`),
}

const Profile = {
    getProfile: (email: string) => axiosInstance.get<IProfile>(`/api/user/user_data/${email}`),
}

const api = {Auth, Cars, Rentals, Profile};

export default api;