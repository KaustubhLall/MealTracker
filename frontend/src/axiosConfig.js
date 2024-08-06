// src/axiosConfig.js
import axios from 'axios';

// Create an Axios instance with a custom config
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api', // Base URL of your API
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;
