// src/components/MealDetailComponent.js
import React, { useEffect, useState } from 'react';
import apiClient from '../axiosConfig';

const MealDetailComponent = ({ meal }) => {
    const [foodComponents, setFoodComponents] = useState([]);

    useEffect(() => {
        const fetchFoodComponents = async () => {
            try {
                const response = await apiClient.get(`/meals/${meal.meal_id}/foodcomponents/`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
                });
                setFoodComponents(response.data);
            } catch (err) {
                console.error(err);
            }
        };

        fetchFoodComponents();
    }, [meal]);

    return (
        <div className="container mt-5">
            <h3>{meal.meal_name} Details</h3>
            <ul>
                {foodComponents.map((component) => (
                    <li key={component.component_id}>
                        {component.food_name}: {component.weight}g
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MealDetailComponent;
