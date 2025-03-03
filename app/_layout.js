import { Slot, useRouter, useSegments } from 'expo-router';
import { useEffect } from 'react';
import { AuthContextProvider, useAuth } from '../context/authcontext';

const MainLayout = () => {
    const { isAuthenticated } = useAuth();
    const segments = useSegments();
    const router = useRouter();

    useEffect(() => {
        if (typeof isAuthenticated === 'undefined') return;

        const inApp = segments[0] === '(app)';

        if (isAuthenticated && !inApp) {
            // If authenticated but not in the app segment, redirect to home
            router.replace('/home');
        } else if (!isAuthenticated && inApp) {
            // If not authenticated and trying to access a protected route, redirect to sign-in
            router.replace('/SignIn');
        }
    }, [isAuthenticated, segments]);

    return <Slot />;
};

export default function Layout() {
    return (
        <AuthContextProvider>
            <MainLayout />
        </AuthContextProvider>
    );
}