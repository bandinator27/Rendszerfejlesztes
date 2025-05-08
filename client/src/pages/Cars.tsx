import {useEffect, useState} from "react";
import api from "../api/api.ts";
import {ICars} from "../interfaces/ICars.ts";
import {Button, Card, Table} from "@mantine/core";
import {useNavigate} from "react-router-dom";

const Cars = () => {
    const [cars, setCars] = useState<ICars[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        api.Cars.getCars().then(res =>{
            console.log(res.data);
            setCars(res.data);
        });
    }, []);

    const rows = cars.map((car) => (
        <Table.Tr key={car.carid}>
            <Table.Td>{car.numberplate}</Table.Td>
            <Table.Td>{car.rentable}</Table.Td>
            <Table.Td>{car.price}</Table.Td>
            <Table.Td>{car.manufacturer}</Table.Td>
            <Table.Td>{car.model}</Table.Td>
            <Table.Td>{car.color}</Table.Td>
            <Table.Td><Button onClick={() => navigate(`${car.carid}`)}>Módosítás</Button></Table.Td>
            <Table.Td><Button onClick={() => navigate(`${car.carid}`)}>Bérlés</Button></Table.Td>
        </Table.Tr>
    ));

    return <>
        <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Button onClick={() => navigate('create')}>Létrehozás</Button>
            <Table>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Rendszám</Table.Th>
                        <Table.Th>Bérelhető</Table.Th>
                        <Table.Th>Ár ($)</Table.Th>
                        <Table.Th>Gyártó</Table.Th>
                        <Table.Th>Model</Table.Th>
                        <Table.Th>Szín</Table.Th>
                        <Table.Th>Műveletek</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>{rows}</Table.Tbody>
            </Table>
        </Card>
    </>
}

export default Cars;