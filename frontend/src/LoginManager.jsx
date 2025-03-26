import { useNavigate } from "react-router-dom";
import icon from "./icon.jpg"
import { useState} from "react";

export default function LoginManager ({setShowRegistrationManager, message, setMessage}) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({email: email, password: password}),
            });
        
            const data = await response.json();
            if (data.logged_in) {
                navigate(data.redirect);
            } else {
                setMessage(data.message)
            }

        } catch (error) {
            console.error('Login failed:', error);
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
                    <form autoComplete="on">
                        <div className="form-group text-start mb-4">
                            <label for="email">Email address:</label>
                            <input type="email" name="email" id="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} className="form-control" placeholder="Enter email"/>
                        </div>
                        <div className="row">
                            <div></div>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label for="password">Password:</label>
                            <input type="password" name="password" id="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} className="form-control" placeholder="Password"/>
                        </div>
                        <div className="row">
                            <p className="text-center text-secondary">
                                {message}
                            </p>
                        </div>
                        <button type="submit" className="btn btn-primary me-4" onClick={handleLogin}>Submit</button>
                        <button type="submit" className="btn btn-secondary" onClick={() => {setShowRegistrationManager(true);setMessage("")}}>Register</button>
                    </form>
                </div>
                <div className="col-4"></div>
            </div>
        </div>
    )
}