import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../axiosConfig';
import Modal from 'react-modal';

Modal.setAppElement('#root'); // To handle modal accessibility

const DashboardComponent = () => {
  const navigate = useNavigate();
  const [goals, setGoals] = useState({
    id: '',
    fat_goal: 0,
    carb_goal: 0,
    protein_goal: 0,
    calorie_goal: 0,
    summary: ''
  });
  const [summaryInput, setSummaryInput] = useState('');
  const [meals, setMeals] = useState([]);
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [newMeal, setNewMeal] = useState({
    meal_name: '',
    time_of_consumption: new Date().toISOString().slice(0, 16)
  });
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
  const [isAddMealVisible, setIsAddMealVisible] = useState(false);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [error, setError] = useState('');

  const fetchGoals = async () => {
    try {
      const response = await apiClient.get('/usergoals/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      if (response.data.length > 0) {
        setGoals({ ...response.data[0], id: response.data[0].user }); // Set goals including the user ID
      }
    } catch (err) {
      console.error('Failed to fetch goals:', err);
      setError('Failed to fetch user goals.');
    }
  };

  const fetchMeals = async (date) => {
    try {
      const response = await apiClient.get('/meals/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      setMeals(response.data);
    } catch (err) {
      console.error('Failed to fetch meals:', err);
      setError('Failed to fetch meals.');
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
    if (meal && meal.meal_id) {
      setSelectedMeal(meal);
      setIsModalOpen(true);
      setError(''); // Clear any previous errors
    } else {
      console.error('Selected meal does not have a valid ID.');
      setError('Selected meal does not have a valid ID.');
    }
  };

  const handleMealUpdate = async (mealId, updatedMeal) => {
    if (!mealId) {
      console.error('No meal ID available for updating.');
      setError('No meal ID available for updating.');
      return;
    }

    try {
      await apiClient.put(`/meals/${mealId}/`, updatedMeal, {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      fetchMeals(selectedDate);
      setIsModalOpen(false);
    } catch (err) {
      console.error('Failed to update meal:', err);
      setError('Failed to update meal.');
    }
  };

  const handleAddComponent = async () => {
    if (!selectedMeal || !selectedMeal.meal_id) {
      console.error('No selected meal to add component to.');
      setError('Please select a meal to add components to.');
      return;
    }

    try {
      await apiClient.post(
        `/foodcomponents/`,
        {
          ...newComponent,
          meal: selectedMeal.meal_id // Use meal_id for the backend
        },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
        }
      );
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
      fetchMeals(selectedDate);
      setIsModalOpen(false);
    } catch (err) {
      console.error('Failed to add component:', err);
      setError('Failed to add food component.');
    }
  };

  const handleAddMeal = async () => {
    try {
      await apiClient.post('/meals/', newMeal, {
        headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
      });
      setNewMeal({
        meal_name: '',
        time_of_consumption: new Date().toISOString().slice(0, 16)
      });
      fetchMeals(selectedDate);
      setIsAddMealVisible(false);
    } catch (err) {
      console.error('Failed to add meal:', err);
      setError('Failed to add meal.');
    }
  };

  const handleSummaryUpdate = async () => {
    if (!goals.id) {
      console.error('No goals ID available for updating.');
      setError('No goals ID available for updating.');
      return;
    }

    try {
      const response = await apiClient.put(
        `/usergoals/${goals.id}/`,
        { summary: summaryInput },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
        }
      );
      setSummaryInput('');
      setError(''); // Clear any errors if successful
      setGoals(response.data); // Update the goals state with the new summary
    } catch (err) {
      console.error('Failed to update summary:', err);
      setError('Failed to update summary.');
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

      {error && <div className="alert alert-danger mt-3">{error}</div>}

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
        <h3>Add New Meal</h3>
        <button
          className="btn btn-primary mb-3"
          onClick={() => setIsAddMealVisible(!isAddMealVisible)}
        >
          {isAddMealVisible ? 'Cancel' : 'Add New Meal'}
        </button>
        {isAddMealVisible && (
          <div className="card p-3 mb-4">
            <div className="form-group">
              <label>Meal Name</label>
              <input
                type="text"
                className="form-control"
                placeholder="Meal Name"
                value={newMeal.meal_name}
                onChange={(e) =>
                  setNewMeal({ ...newMeal, meal_name: e.target.value })
                }
              />
            </div>
            <div className="form-group">
              <label>Time of Consumption</label>
              <input
                type="datetime-local"
                className="form-control"
                value={newMeal.time_of_consumption}
                onChange={(e) =>
                  setNewMeal({
                    ...newMeal,
                    time_of_consumption: e.target.value
                  })
                }
              />
            </div>
            <button className="btn btn-primary mt-2" onClick={handleAddMeal}>
              Add Meal
            </button>
          </div>
        )}
      </div>

      <div className="mt-4">
        <h3>Meals for {selectedDate}</h3>
        {meals.length === 0 ? (
          <p>No meals logged for this day.</p>
        ) : (
          <div className="row">
            {meals.map((meal) => (
              <div className="col-md-4" key={meal.meal_id}>
                <div className="card mb-3">
                  <div className="card-body">
                    <h5 className="card-title">{meal.meal_name}</h5>
                    <p className="card-text">
                      <strong>Time of Consumption:</strong>{' '}
                      {new Date(meal.time_of_consumption).toLocaleString()}
                    </p>
                    <p className="card-text">
                      <strong>Hunger Level:</strong> {meal.hunger_level}
                    </p>
                    <p className="card-text">
                      <strong>Exercise:</strong> {meal.exercise}
                    </p>
                    <p className="card-text">
                      <strong>Total Calories:</strong> {meal.total_calories}
                    </p>
                    <p className="card-text">
                      <strong>Total Fat:</strong> {meal.total_fat}g
                    </p>
                    <p className="card-text">
                      <strong>Total Protein:</strong> {meal.total_protein}g
                    </p>
                    <p className="card-text">
                      <strong>Total Carbs:</strong> {meal.total_carbs}g
                    </p>
                    <p className="card-text">
                      <strong>Total Sugar:</strong> {meal.total_sugar}g
                    </p>
                    <button
                      className="btn btn-link"
                      onClick={() => handleMealSelect(meal)}
                    >
                      View/Edit
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Modal isOpen={isModalOpen} onRequestClose={() => setIsModalOpen(false)}>
        <h2>Edit Meal: {selectedMeal?.meal_name}</h2>
        {selectedMeal && (
          <div>
            <div className="form-group">
              <label>Meal Name</label>
              <input
                type="text"
                className="form-control"
                value={selectedMeal.meal_name}
                onChange={(e) =>
                  setSelectedMeal({ ...selectedMeal, meal_name: e.target.value })
                }
              />
            </div>
            <div className="form-group">
              <label>Time of Consumption</label>
              <input
                type="datetime-local"
                className="form-control"
                value={new Date(selectedMeal.time_of_consumption)
                  .toISOString()
                  .slice(0, 16)}
                onChange={(e) =>
                  setSelectedMeal({
                    ...selectedMeal,
                    time_of_consumption: e.target.value
                  })
                }
              />
            </div>
            <button
              className="btn btn-success mt-2"
              onClick={() =>
                handleMealUpdate(selectedMeal.meal_id, selectedMeal)
              }
            >
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
            <button
              className="btn btn-primary mt-3"
              onClick={() => setIsModalOpen(false)}
            >
              Add Food Component
            </button>
          </div>
        )}
        <button
          className="btn btn-secondary mt-2"
          onClick={() => setIsModalOpen(false)}
        >
          Close
        </button>
      </Modal>
    </div>
  );
};

export default DashboardComponent;
