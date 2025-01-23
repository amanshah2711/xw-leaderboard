import icon from "./icon.jpg"
import { useState } from "react";

export default function Login ({info, update}) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/api/login', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({email: email, password: password}),
            });
        
            const data = await response.json();
        
            if (response.ok) {
                update(data);
            } else {
                console.log("failure");
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
                <form>
                    <div className="form-group text-start mb-4">
                        <label>Email address:</label>
                        <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email"/>
                    </div>
                    <div className="row">
                        <div></div>
                    </div>
                    <div className="form-group text-start mb-4">
                        <label>Password:</label>
                        <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} className="form-control" id="exampleInputPassword1" placeholder="Password"/>
                    </div>
                    <div className="row">
                        <p className="text-center text-secondary">
                            {info.message}
                        </p>
                    </div>
                    <button type="submit" className="btn btn-primary me-4" onClick={handleLogin}>Submit</button>
                    <button type="submit" className="btn btn-secondary" onClick={() => {update({"registration" : !info.registration, "message" : ""})}}>Register</button>
                </form>
            </div>
        </div>
    )
}