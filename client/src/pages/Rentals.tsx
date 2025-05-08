import {useEffect, useState} from "react";
import api from "../api/api.ts";
import {IRentals} from "../interfaces/IRentals.ts";
import {Button, Card, Table} from "@mantine/core";
import {useNavigate} from "react-router-dom";

const Rentals = () => {
    const [rentals, setRentals] = useState<IRentals[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        api.Rentals.getRentals().then(res =>{
            console.log(res.data);
            setRentals(res.data);
        });
    }, []);

    const rows = rentals.map((rental) => (
        <Table.Tr key={rental.carid}>
            <Table.Td>{rental.renterid}</Table.Td>
            <Table.Td>{rental.rentedat}</Table.Td>
            <Table.Td>{rental.rentstatus}</Table.Td>
            <Table.Td>{rental.rentduration}</Table.Td>
            <Table.Td>{rental.rentprice}</Table.Td>
            <Table.Td>{rental.renteraddress}</Table.Td>
            <Table.Td>{rental.renterphonenum}</Table.Td>
            <Table.Td><Button onClick={() => navigate(`${rental.carid}`)}>Módosítás</Button></Table.Td>
        </Table.Tr>
    ));

    return <>
        <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Button onClick={() => navigate('create')}>Létrehozás</Button>
            <Table>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Bérlő ID</Table.Th>
                        <Table.Th>Bérelve</Table.Th>
                        <Table.Th>Bérlés állapot</Table.Th>
                        <Table.Th>Bérlés időtartam</Table.Th>
                        <Table.Th>Bérlés ár</Table.Th>
                        <Table.Th>Bérlő címe</Table.Th>
                        <Table.Th>Bérlő telefonszáma</Table.Th>
                        <Table.Th>Műveletek</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>{rows}</Table.Tbody>
            </Table>
        </Card>
    </>
}

export default Rentals;