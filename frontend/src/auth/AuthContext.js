import { createContext, useEffect, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    // THIS IS IMPORTANT:
    // The commented code below allows the user to be stored in the local storage
    // currently its not stored in purpose cause backend is not implemented yet
    
    // useEffect(() => {
    //   const storedUser = localStorage.getItem('user');
    //   if (storedUser) {
    //     setUser(JSON.parse(storedUser));
    //   }
    // }, []);
    
    const login = (userData) => {
        setUser(userData);
        // localStorage.setItem('user', JSON.stringify(userData));
    };

    const logout = () => {
        setUser(null);
        // localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
