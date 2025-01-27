import { useState, useEffect } from "react"
import RegistrationManager from "./RegistrationManager";
import LoginManager from "./LoginManager";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
    const [showRegistrationManager, setShowRegistrationManager] = useState(false);
    const [message, setMessage] = useState("");
    const navigate = useNavigate();
    useEffect (() => {
    const checkLogin = async () => {
        try {
            const response = await fetch('/api/check_login', {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });
        
            const data = await response.json();
            if (data.logged_in) {
                navigate('/leaderboard')
            }

        } catch (error) {
            console.error('Checking if user is already logged in failed:', error);
        }
    }; 
    checkLogin()
    }, []);
    return (
        <div>
            {showRegistrationManager ? 
                <RegistrationManager setShowRegistrationManager={setShowRegistrationManager} message={message} setMessage={setMessage}/> : 
                <LoginManager setShowRegistrationManager={setShowRegistrationManager} message={message} setMessage={setMessage}/>
                }
        </div>
    )
}