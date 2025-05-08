import {Center, Divider, Image, Paper, Text} from "@mantine/core";

interface AuthContainerInterface {
    children: JSX.Element;
}

const AuthContainer = ({children}: AuthContainerInterface) => {
    return <div className="auth-container">
        <Center><Image src="/logo.png" alt="img" w={150} mt={30}/></Center>
        <Center>
            <Paper radius="md" p="xl" withBorder maw={600} m={10}>
                <Text size="lg" fw={500}>
                    Üdvözlünk a Bérautó felületen
                </Text>
                <Divider my="lg"/>
                {children}
            </Paper>
        </Center>
    </div>
}

export default AuthContainer;