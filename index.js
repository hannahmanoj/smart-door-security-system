import { registerRootComponent } from 'expo';
import { ExpoRoot } from 'expo-router';

export default function Main() {
    return <ExpoRoot />;
}

registerRootComponent(Main);
