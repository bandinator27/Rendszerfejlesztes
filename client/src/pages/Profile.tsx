import {useContext, useEffect, useState} from "react";
import api from "../api/api.ts";
import {IProfile} from "../interfaces/IProfile.ts";
import {Button, Card, Table} from "@mantine/core";
import {useNavigate} from "react-router-dom";
import {AuthContext} from "../context/AuthContext.tsx";

const Profile = () => {
    const [profile, setProfile] = useState<IProfile[]>([]);
    const navigate = useNavigate();
    const {email} = useContext(AuthContext);

    useEffect(() => {
        if (email !== null) {
            api.Profile.getProfile(email).then(res =>{
                console.log(res.data);
                //setProfile(res.data);
            });
        }
    }, []);

    const rows = profile.map((prof) => (
        <Table.Tr key={prof.id}>
            <Table.Td>{prof.username}</Table.Td>
            <Table.Td>{prof.email}</Table.Td>
            <Table.Td>{prof.city}</Table.Td>
            <Table.Td>{prof.street}</Table.Td>
            <Table.Td>{prof.postalcode}</Table.Td>
            <Table.Td><Button onClick={() => navigate(`${prof.id}`)}>Módosítás</Button></Table.Td>
        </Table.Tr>
    ));

    return <>
        <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Button onClick={() => navigate('create')}>Létrehozás</Button>
            <Table>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Felhasználónév</Table.Th>
                        <Table.Th>E-mail</Table.Th>
                        <Table.Th>Város</Table.Th>
                        <Table.Th>Utca</Table.Th>
                        <Table.Th>Körzetkód</Table.Th>
                        <Table.Th>Műveletek</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>{rows}</Table.Tbody>
            </Table>
        </Card>
    </>
}

export default Profile;