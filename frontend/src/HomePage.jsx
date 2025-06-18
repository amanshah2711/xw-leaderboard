import { useState, useEffect } from "react"
import RegistrationManager from "./RegistrationManager";
import LoginManager from "./LoginManager";
import { useNavigate } from "react-router-dom";
import { useFetch } from "./services/useFetch.jsx"

export default function HomePage() {
    const [showRegistrationManager, setShowRegistrationManager] = useState(false);
    const [message, setMessage] = useState("");
    const navigate = useNavigate();
    const { data, loading, error } = useFetch("/api/check-login");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    if (data.logged_in) {
        navigate('/daily');
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