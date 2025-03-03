import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthContextProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // TODO: Implement real authentication logic (e.g., AsyncStorage, Firebase)
        setTimeout(() => setIsAuthenticated(false), 1000); // Default: Not Authenticated
    }, []);

    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
