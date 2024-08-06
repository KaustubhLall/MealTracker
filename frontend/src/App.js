// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginComponent from './components/LoginComponent';
import RegisterComponent from './components/RegisterComponent';
import GoalsComponent from './components/GoalsComponent';
import MealsComponent from './components/MealsComponent';
import MealDetailComponent from './components/MealDetailComponent';
import DashboardComponent from './components/DashboardComponent';

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [selectedMeal, setSelectedMeal] = useState(null);

    useEffect(() => {
        // Check if the user is already logged in
        const accessToken = localStorage.getItem('accessToken');
        if (accessToken) {
            setIsAuthenticated(true);
        }
    }, []);

    const handleLogin = () => {
        setIsAuthenticated(true);
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginComponent onLogin={handleLogin} />} />
                <Route path="/register" element={<RegisterComponent />} />
                <Route path="/dashboard" element={isAuthenticated ? <DashboardComponent /> : <Navigate to="/login" />} />
                <Route path="/goals" element={isAuthenticated ? <GoalsComponent /> : <Navigate to="/login" />} />
                <Route path="/meals" element={isAuthenticated ? <MealsComponent onMealSelect={setSelectedMeal} /> : <Navigate to="/login" />} />
                <Route path="/meal-detail" element={selectedMeal ? <MealDetailComponent meal={selectedMeal} /> : <Navigate to="/meals" />} />
                <Route path="/" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
};

export default App;
