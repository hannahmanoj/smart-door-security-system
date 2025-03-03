import { View, Button } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomePage() {
    const router = useRouter();

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Button title="Go to Sign In" onPress={() => router.push('/SignIn')} />
        </View>
    );
}
