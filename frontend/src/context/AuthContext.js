import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error('Failed to parse stored user data', e);
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  // For demo purposes, we'll use a simplified login function
  // In a real application, this would make an API call to authenticate
  const login = async (username, password) => {
    setLoading(true);
    setError(null);
    
    try {
      // In a real app, this would be an API call
      // For demo, we'll simulate authentication with demo users
      const demoUsers = {
        admin: {
          id: 1,
          username: 'admin',
          fullName: 'Admin User',
          role: 'admin',
          department: 'IT'
        },
        sales_manager: {
          id: 2,
          username: 'sales_manager',
          fullName: 'Sales Manager',
          role: 'manager',
          department: 'Sales'
        },
        production_manager: {
          id: 3,
          username: 'production_manager',
          fullName: 'Production Manager',
          role: 'manager',
          department: 'Production'
        },
        inventory_manager: {
          id: 4,
          username: 'inventory_manager',
          fullName: 'Inventory Manager',
          role: 'manager',
          department: 'Inventory'
        },
        sales_rep: {
          id: 5,
          username: 'sales_rep',
          fullName: 'Sales Representative',
          role: 'sales',
          department: 'Sales'
        }
      };
      
      // Check if username exists and password is 'secret'
      if (demoUsers[username] && password === 'secret') {
        const userData = demoUsers[username];
        
        // Add token (in real app would come from server)
        userData.token = 'demo-token-' + Math.random().toString(36).substring(2);
        
        // Store user data
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Configure axios to use the token for future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${userData.token}`;
        
        return userData;
      } else {
        throw new Error('Invalid username or password');
      }
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};