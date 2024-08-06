// src/components/DashboardComponent.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../axiosConfig';
import Modal from 'react-modal';

Modal.setAppElement('#root'); // To handle modal accessibility

const DashboardComponent = () => {
    const navigate = useNavigate();
    const [goals, setGoals] = useState({ fat_goal: 0, carb_goal: 0, protein_goal: 0, calorie_goal: 0, summary: '' });
    const [summaryInput, setSummaryInput] = useState('');
    const [meals, setMeals] = useState([]);
    const [selectedMeal, setSelectedMeal] = useState(null);
    const [newMeal, setNewMeal] = useState({ meal_name: '', time_of_consumption: '' });
    const [newComponent, setNewComponent] = useState({
        food_name: '',
        brand: '',
        weight: 0,
        fat: 0,
        protein: 0,
        carbs: 0,
        sugar: 0,
        total_calories: 0,
        micronutrients: {}
    });
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

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

    const fetchMeals = async (date) => {
        try {
            const response = await apiClient.get(`/meals/?date=${date}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setMeals(response.data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchGoals();
        fetchMeals(selectedDate);
    }, [selectedDate]);

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        window.location.reload(); // Refresh the page to effectively log out
    };

    const handleMealSelect = (meal) => {
        setSelectedMeal(meal);
    };

    const handleMealUpdate = async (meal_id, updatedMeal) => {
        try {
            await apiClient.put(`/meals/${meal_id}/`, updatedMeal, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            fetchMeals(selectedDate);
        } catch (err) {
            console.error(err);
        }
    };

    const handleAddComponent = async () => {
        try {
            await apiClient.post(`/meals/${selectedMeal.meal_id}/foodcomponents/`, newComponent, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setNewComponent({
                food_name: '',
                brand: '',
                weight: 0,
                fat: 0,
                protein: 0,
                carbs: 0,
                sugar: 0,
                total_calories: 0,
                micronutrients: {}
            });
            fetchMeals(selectedDate); // Refresh meals to update the meal statistics
            setIsModalOpen(false);
        } catch (err) {
            console.error(err);
        }
    };

    const handleAddMeal = async () => {
        try {
            await apiClient.post('/meals/', newMeal, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setNewMeal({ meal_name: '', time_of_consumption: '' });
            fetchMeals(selectedDate);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSummaryUpdate = async () => {
        try {
            await apiClient.post('/usergoals/update-summary/', { summary: summaryInput }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setSummaryInput('');
            fetchGoals();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="container mt-5">
            <div className="d-flex justify-content-between align-items-center">
                <h2>Your Dashboard</h2>
                <button onClick={handleLogout} className="btn btn-danger">
                    Logout
                </button>
            </div>

            <div className="mt-4">
                <h3>Your Goals</h3>
                <p>Summary: {goals.summary}</p>
                <ul>
                    <li>Fat Goal: {goals.fat_goal}</li>
                    <li>Carb Goal: {goals.carb_goal}</li>
                    <li>Protein Goal: {goals.protein_goal}</li>
                    <li>Calorie Goal: {goals.calorie_goal}</li>
                </ul>
                <input
                    type="text"
                    className="form-control"
                    placeholder="Update Summary"
                    value={summaryInput}
                    onChange={(e) => setSummaryInput(e.target.value)}
                />
                <button className="btn btn-primary mt-2" onClick={handleSummaryUpdate}>
                    Update Summary
                </button>
            </div>

            <div className="mt-4">
                <h3>Select Date</h3>
                <input
                    type="date"
                    className="form-control"
                    value={selectedDate}
                    onChange={(e) => setSelectedDate(e.target.value)}
                />
            </div>

            <div className="mt-4">
                <h3>Meals for {selectedDate}</h3>
                {meals.length === 0 ? (
                    <p>No meals logged for this day.</p>
                ) : (
                    <ul>
                        {meals.map((meal) => (
                            <li key={meal.meal_id}>
                                {meal.meal_name} - {new Date(meal.time_of_consumption).toLocaleTimeString()}
                                <button className="btn btn-link" onClick={() => handleMealSelect(meal)}>
                                    View/Edit
                                </button>
                            </li>
                        ))}
                    </ul>
                )}

                <div className="mt-4">
                    <h4>Add New Meal</h4>
                    <div className="form-group">
                        <label>Meal Name</label>
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Meal Name"
                            value={newMeal.meal_name}
                            onChange={(e) => setNewMeal({ ...newMeal, meal_name: e.target.value })}
                        />
                    </div>
                    <div className="form-group">
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
            </div>

            {selectedMeal && (
                <div className="mt-4 card p-3">
                    <h4>Edit Meal: {selectedMeal.meal_name}</h4>
                    <div className="form-group">
                        <label>Meal Name</label>
                        <input
                            type="text"
                            className="form-control"
                            value={selectedMeal.meal_name}
                            onChange={(e) => setSelectedMeal({ ...selectedMeal, meal_name: e.target.value })}
                        />
                    </div>
                    <div className="form-group">
                        <label>Time of Consumption</label>
                        <input
                            type="datetime-local"
                            className="form-control"
                            value={new Date(selectedMeal.time_of_consumption).toISOString().substring(0, 16)}
                            onChange={(e) => setSelectedMeal({ ...selectedMeal, time_of_consumption: e.target.value })}
                        />
                    </div>
                    <button className="btn btn-success mt-2" onClick={() => handleMealUpdate(selectedMeal.meal_id, selectedMeal)}>
                        Save Changes
                    </button>

                    <h5 className="mt-4">Food Components</h5>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Weight (g)</th>
                                <th>Calories (kcal)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {selectedMeal.food_components?.map((component) => (
                                <tr key={component.component_id}>
                                    <td>{component.food_name}</td>
                                    <td>{component.weight}</td>
                                    <td>{component.total_calories}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <button className="btn btn-primary mt-3" onClick={() => setIsModalOpen(true)}>
                        Add Food Component
                    </button>
                </div>
            )}

            <Modal isOpen={isModalOpen} onRequestClose={() => setIsModalOpen(false)}>
                <h2>Add Food Component</h2>
                <div className="form-group">
                    <label>Food Name</label>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Food Name"
                        value={newComponent.food_name}
                        onChange={(e) => setNewComponent({ ...newComponent, food_name: e.target.value })}
                    />
                    <label>Brand</label>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Brand"
                        value={newComponent.brand}
                        onChange={(e) => setNewComponent({ ...newComponent, brand: e.target.value })}
                    />
                    <label>Weight (g)</label>
                    <input
                        type="number"
                        className="form-control"
                        placeholder="Weight"
                        value={newComponent.weight}
                        onChange={(e) => setNewComponent({ ...newComponent, weight: parseFloat(e.target.value) })}
                    />
                    <label>Fat (g)</label>
                    <input
                        type="number"
                        className="form-control"
                        placeholder="Fat"
                        value={newComponent.fat}
                        onChange={(e) => setNewComponent({ ...newComponent, fat: parseFloat(e.target.value) })}
                    />
                    <label>Protein (g)</label>
                    <input
                        type="number"
                        className="form-control"
                        placeholder="Protein"
                        value={newComponent.protein}
                        onChange={(e) => setNewComponent({ ...newComponent, protein: parseFloat(e.target.value) })}
                    />
                    <label>Carbs (g)</label>
                    <input
                        type="number"
                        className="form-control"
                        placeholder="Carbs"
                        value={newComponent.carbs}
                        onChange={(e) => setNewComponent({ ...newComponent, carbs: parseFloat(e.target.value) })}
                    />
                    <label>Sugar (g)</label>
                    <input
                        type="number"
                        className="form-control"
                        placeholder="Sugar"
                        value={newComponent.sugar}
                        onChange={(e) => setNewComponent({ ...newComponent, sugar: parseFloat(e.target.value) })}
                    />
                    <label>Total Calories (kcal)</label>
                    <input
                        type="number"
                        className="form-control"
                        placeholder="Total Calories"
                        value={newComponent.total_calories}
                        onChange={(e) => setNewComponent({ ...newComponent, total_calories: parseFloat(e.target.value) })}
                    />
                    <label>Micronutrients (JSON)</label>
                    <textarea
                        className="form-control"
                        placeholder='{"Vitamin C": 10, "Iron": 2}'
                        value={JSON.stringify(newComponent.micronutrients)}
                        onChange={(e) => setNewComponent({ ...newComponent, micronutrients: JSON.parse(e.target.value || '{}') })}
                    />
                </div>
                <button className="btn btn-primary mt-2" onClick={handleAddComponent}>
                    Add Component
                </button>
                <button className="btn btn-secondary mt-2" onClick={() => setIsModalOpen(false)}>
                    Cancel
                </button>
            </Modal>
        </div>
    );
};

export default DashboardComponent;
