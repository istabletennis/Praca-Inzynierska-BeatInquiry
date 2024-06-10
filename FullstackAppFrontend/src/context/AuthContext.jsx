import React, { createContext, useContext, useState } from 'react';
import axios from '../api/axiosConfig';
import qs from 'qs';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (username, password) => {
    try {
      const response = await axios.post(
      '/token',
      qs.stringify({ username, password }),
       {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
            },
        }
      );
      const { access_token } = response.data;
      setUser({ username, access_token });
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
  };

  const register = async (username, password) => {
    try {
      const response = await axios.post(
        '/register',
        { username: username, password: password},
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        );
      const { username: userResp } = response.data;
      setUser({ username: userResp });
      // Log in the user immediately after registration
      await login(username, password);
    } catch (error) {
      console.error("Registration failed:", error);
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
