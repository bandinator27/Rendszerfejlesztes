import {Button, Card, Group, NativeSelect, NumberInput, TextInput} from "@mantine/core";
import {useForm} from "@mantine/form";
import {useEffect, useState} from "react";
import api from "../api/api.ts";
import {IRestaurant} from "../interfaces/IRestaurant.ts";
import {useParams} from "react-router-dom";

interface ICreateUpdateFoods {
    isCreate: boolean
}

const CreateUpdateFoods = ({isCreate}: ICreateUpdateFoods) => {
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            name: '',
            description: '',
            price: 0,
            foodCategoryId: '',
            restaurantId: ''
        },

        validate: {
            // name: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
            name: (value) => (value.length <= 3 ? 'Legalább 3 karakter hosszúnak kell lennie' : null),
            description: (value) => (value.length <= 3 ? 'Legalább 3 karakter hosszúnak kell lennie' : null),
            price: (value) => (value < 0 ? 'Az ár nem lehet kisebb, mint 0Ft.': null)
        },
    });

    const [categories, setCategories] = useState<{name: string, id: number}[]>([]);
    const [restaurants, setRestaurants] = useState<IRestaurant[]>([]);
    const { id } = useParams();

    useEffect(() => {
        api.Food.getCategories().then(res => setCategories(res.data));
        api.Restaurant.getRestaurants().then(res => setRestaurants(res.data));
    }, []);

    useEffect(() => {
        if (id && !isCreate) {
            api.Food.getFood(String(id)).then(res => {
                form.initialize({
                    foodCategoryId: res.data.category?.id.toString(),
                    restaurantId: res.data.restaurant?.id.toString(),
                    price: res.data.price,
                    name: res.data.name,
                    description: res.data.description
                });
            });
        }
    }, [id, isCreate]);

    return <>
        <Card>
            <form onSubmit={form.onSubmit((values) => {
                if (isCreate) {
                    api.Food.createFood(
                        {
                            name: values.name,
                            description: values.description,
                            price: values.price,
                            foodCategoryId: Number(values.foodCategoryId),
                            restaurantId: Number(values.restaurantId)
                        }
                    ).then();
                } else {
                    api.Food.updateFood(String(id),
                        {
                            name: values.name,
                            description: values.description,
                            price: values.price,
                            foodCategoryId: Number(values.foodCategoryId)
                        }
                    ).then();
                }

            })}>
                <TextInput
                    withAsterisk
                    label="Név"
                    placeholder="Név"
                    key={form.key('name')}
                    {...form.getInputProps('name')}
                />

                <TextInput
                    withAsterisk
                    label="Leírás"
                    placeholder="Leírás"
                    key={form.key('description')}
                    {...form.getInputProps('description')}
                />

                <NumberInput
                    withAsterisk
                    label="Ár"
                    placeholder="Ár"
                    key={form.key('price')}
                    {...form.getInputProps('price')} />

                <NativeSelect
                    label="Kategória"
                    description="Étel kategória"
                    key={form.key('foodCategoryId')}
                    {...form.getInputProps('foodCategoryId')}
                    data={categories.map((c) => {
                        return {
                            value: c.id.toString(),
                            label: c.name,
                        }
                    })}
                />

                <NativeSelect
                    label="Étterem"
                    description="Étterem"
                    key={form.key('restaurantId')}
                    {...form.getInputProps('restaurantId')}
                    data={restaurants.map((c) => {
                        return {
                            value: c.id.toString(),
                            label: c.name,
                        }
                    })}
                />

                <Group justify="flex-end" mt="md">
                    <Button type="submit">Mentés</Button>
                </Group>
            </form>
        </Card>

    </>
}

export default CreateUpdateFoods;