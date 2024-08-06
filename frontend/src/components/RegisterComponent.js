// src/components/RegisterComponent.js
import React, { useState } from 'react';
import apiClient from '../axiosConfig';

const RegisterComponent = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await apiClient.post('/register/', { username, password, email });
            setSuccess(true);
            setError('');
        } catch (err) {
            setError('Registration failed');
            console.error('Registration error:', err);
        }
    };

    return (
        <div className="container mt-5">
            <h2>Register</h2>
            {success ? (
                <p className="text-success">
                    Registration successful! <a href="/login">Login</a>
                </p>
            ) : (
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            className="form-control"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            className="form-control"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    {error && <p className="text-danger">{error}</p>}
                    <button type="submit" className="btn btn-primary">Register</button>
                </form>
            )}
        </div>
    );
};

export default RegisterComponent;
