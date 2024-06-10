import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:8000', // Your FastAPI server address
    headers: {
        'Content-Type': 'application/json'
    }
});

export default instance;
