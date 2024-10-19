import React, { useState } from 'react';
import axios from 'axios';

const Registration = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState(''); // State for password
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        setErrorMessage('');
        setSuccessMessage('');

        try {
            const response = await axios.post("http://localhost:8000/register", {
                username,
                password, // Include password in the request
            });

            setSuccessMessage("Registration successful! Please log in.");
            setUsername('');
            setPassword(''); // Clear password after registration
        } catch (error) {
            if (error.response) {
                setErrorMessage(error.response.data.detail);
            } else {
                setErrorMessage("Registration failed. Please try again.");
            }
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleRegister}>
                <input
                    type="text"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password" // Password input type
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Register</button>
            </form>
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
        </div>
    );
};

export default Registration;
