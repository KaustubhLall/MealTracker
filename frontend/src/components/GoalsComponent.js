// src/components/GoalsComponent.js
import React, { useState, useEffect } from 'react';
import apiClient from '../axiosConfig';

const GoalsComponent = () => {
    const [goals, setGoals] = useState({ fat_goal: 0, carb_goal: 0, protein_goal: 0, calorie_goal: 0 });
    const [inputGoals, setInputGoals] = useState('');

    const fetchGoals = async () => {
        try {
            const response = await apiClient.get('/usergoals/', {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setGoals(response.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchGoals();
    }, []);

    const handleUpdateGoals = async () => {
        try {
            await apiClient.post('/usergoals/', { goals_input: inputGoals }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            alert('Goals updated successfully');
            setInputGoals('');
            fetchGoals();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="container mt-5">
            <h2>Your Goals</h2>
            <ul>
                <li>Fat Goal: {goals.fat_goal}</li>
                <li>Carb Goal: {goals.carb_goal}</li>
                <li>Protein Goal: {goals.protein_goal}</li>
                <li>Calorie Goal: {goals.calorie_goal}</li>
            </ul>
            <div className="form-group">
                <label>Update Goals</label>
                <input
                    type="text"
                    className="form-control"
                    value={inputGoals}
                    onChange={(e) => setInputGoals(e.target.value)}
                />
            </div>
            <button className="btn btn-primary" onClick={handleUpdateGoals}>Update</button>
        </div>
    );
};

export default GoalsComponent;
