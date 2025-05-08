import {
    Stack,
    TextInput,
    PasswordInput,
    Group,
    Button,
    Anchor, Divider
} from "@mantine/core";
import {useForm} from "@mantine/form";
import {useNavigate} from "react-router-dom";
import AuthContainer from "../components/AuthContainer.tsx";
import useAuth from "../hooks/useAuth.tsx";

const Login = () => {
    const {login} = useAuth();
    const navigate = useNavigate();

    const form = useForm({
        initialValues: {
            email: '',
            password: '',
        },

        validate: {
            email: (val: string) => (/^\S+@\S+$/.test(val) ? null : 'Érvénytelen e-mail cím'),
            password: (val: string) => (val.length <= 6 ? 'A jelszónak 6 karakter hosszúnak kell lennie.' : null),
        },
    });


    const submit = () => {
        login(form.values.email, form.values.password)
    }

    return <AuthContainer>
        <div>
            <form onSubmit={form.onSubmit(submit)}>
                <Stack>
                    <TextInput
                        required
                        label="E-mail cím"
                        placeholder="hello@mantine.dev"
                        key={form.key('email')}
                        radius="md"
                        {...form.getInputProps('email')}
                    />

                    <PasswordInput
                        required
                        label="Jelszó"
                        placeholder="Jelszavad"
                        key={form.key('password')}
                        radius="md"
                        {...form.getInputProps('password')}
                    />
                </Stack>

                <Group justify="space-between" mt="xl">
                    <Anchor component="button" type="button" c="dimmed" onClick={() => navigate('/forgot')}
                            size="xs">
                        Elfelejtetted a jelszavad?
                    </Anchor>
                    <Button type="submit" radius="xl">
                        Bejelentkezés
                    </Button>
                </Group>
                <Divider my="lg"/>
            </form>
        </div>
    </AuthContainer>
}

export default Login;