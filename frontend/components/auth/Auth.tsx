// frontend/Auth.tsx
import React from 'react';

const exchangeOAuthLogin = () => {
    window.location.href = "https://your-backend.com/auth/login";
};

export default function Login() {
    return (
        <div>
            <button onClick={exchangeOAuthLogin}>Login with Exchange</button>
        </div>
    );
}