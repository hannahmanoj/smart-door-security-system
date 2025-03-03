import { View, Text, Button } from 'react-native';
import { useRouter } from 'expo-router';

export default function SignIn() {
    const router = useRouter();

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text>Sign In Page</Text>
            <Button title="Go to Sign Up" onPress={() => router.push('/SignUp')} />
        </View>
    );
}
