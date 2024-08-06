// src/components/DashboardComponent.js
import React from 'react';
import { Link } from 'react-router-dom';

const DashboardComponent = () => {
    return (
        <div className="container mt-5">
            <h2>Welcome to Your Dashboard</h2>
            <p>Here you can manage your meals and goals.</p>
            <div className="mt-4">
                <Link to="/goals" className="btn btn-primary mr-2">
                    Manage Goals
                </Link>
                <Link to="/meals" className="btn btn-secondary">
                    View Meals
                </Link>
            </div>
        </div>
    );
};

export default DashboardComponent;
