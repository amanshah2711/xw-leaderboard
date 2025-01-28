
import { useNavigate } from "react-router-dom";
import icon from "./icon.jpg";
import { useState } from "react";

export default function RegistrationManager({setShowRegistrationManager, message, setMessage}) {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const navigate = useNavigate();
    const handleRegistration = async (e) => {
        e.preventDefault();
        if (password != confirmPassword) {
            setMessage("Passwords don't match!")
        } else {
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({email: email, password: password, username: username}),
                });
            
                const data = await response.json();
            
                if (response.ok) {
                    if (data.success) {
                        setShowRegistrationManager(false);
                    }
                    setMessage(data.message);
                } else {
                    console.log("failure");
                }
            }
            catch (error) {
                console.error('Submitting Registration Information Failed:', error);
            }
    }
    };  
    return (
        <div>
            <div className="row justify-content-center">
                <img src={icon} className="img-fluid" style={{ maxWidth: "300px", height: "auto" }}></img>
            </div>
            <div className="row">
                <div className="col-4"></div>
                <div className="col-4">
                    <form>
                        <div className="form-group text-start mb-4">
                            <label>Email address:</label>
                            <input value={email} onChange={(e) => setEmail(e.target.value)} className="form-control" placeholder="Enter email"/>
                        </div>
                        <div className="row">
                            <div></div>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label>Username:</label>
                            <input value={username} onChange={(e) => setUsername(e.target.value)} className="form-control" placeholder="Username"/>
                        </div>
                        <div className="row">
                            <div></div>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label>Password:</label>
                            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="form-control" minLength="8" placeholder="Password"/>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label>Password:</label>
                            <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="form-control" minLength="8" placeholder="Verify Password"/>
                        </div>
                        <div className="row">
                            <p className="text-center text-danger">
                                {message} 
                            </p>
                        </div>
                        <button type="submit" className="btn btn-primary me-4" onClick={handleRegistration}>Submit</button>
                        <button type="submit" className="btn btn-secondary" onClick={() => {setShowRegistrationManager(false); setMessage("")}}>Back</button>
                    </form>
                </div>
            <div className="col-4"></div>
            </div>
        </div>
    )
}