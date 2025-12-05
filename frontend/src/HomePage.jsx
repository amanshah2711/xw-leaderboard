import { useState, useEffect } from "react";
import RegistrationManager from "./RegistrationManager";
import LoginManager from "./LoginManager";
import { useNavigate, useLocation } from "react-router-dom";
import { useFetch } from "./services/useFetch.jsx"

export default function HomePage() {
    const [showRegistrationManager, setShowRegistrationManager] = useState(false);
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const status = queryParams.get('message');
    const [message, setMessage] = useState(status);
    const navigate = useNavigate();
    const { data, loading, error } = useFetch("/api/auth/check-login");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    if (!loading && data.logged_in) {
        navigate('/nyt-daily');
    } 
    return (
        <div>
            {showRegistrationManager ? 
                <RegistrationManager setShowRegistrationManager={setShowRegistrationManager} message={message} setMessage={setMessage}/> : 
                <LoginManager setShowRegistrationManager={setShowRegistrationManager} message={message} setMessage={setMessage}/>
                }
        </div>
    )
}
