// src/components/MealsComponent.js
import React, { useState, useEffect } from 'react';
import apiClient from '../axiosConfig';

const MealsComponent = ({ onMealSelect }) => {
    const [meals, setMeals] = useState([]);
    const [newMeal, setNewMeal] = useState({ meal_name: '', time_of_consumption: '' });

    const fetchMeals = async () => {
        try {
            const response = await apiClient.get('/meals/', {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setMeals(response.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchMeals();
    }, []);

    const handleAddMeal = async () => {
        try {
            await apiClient.post('/meals/', newMeal, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setNewMeal({ meal_name: '', time_of_consumption: '' });
            fetchMeals();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="container mt-5">
            <h2>Today's Meals</h2>
            {meals.length === 0 ? (
                <p>No meals logged.</p>
            ) : (
                <ul>
                    {meals.map((meal) => (
                        <li key={meal.meal_id} onClick={() => onMealSelect(meal)}>
                            {meal.meal_name} - {new Date(meal.time_of_consumption).toLocaleTimeString()}
                        </li>
                    ))}
                </ul>
            )}
            <div className="form-group mt-4">
                <label>New Meal Name</label>
                <input
                    type="text"
                    className="form-control"
                    value={newMeal.meal_name}
                    onChange={(e) => setNewMeal({ ...newMeal, meal_name: e.target.value })}
                />
                <label>Time of Consumption</label>
                <input
                    type="datetime-local"
                    className="form-control"
                    value={newMeal.time_of_consumption}
                    onChange={(e) => setNewMeal({ ...newMeal, time_of_consumption: e.target.value })}
                />
            </div>
            <button className="btn btn-primary mt-2" onClick={handleAddMeal}>
                Add Meal
            </button>
        </div>
    );
};

export default MealsComponent;
