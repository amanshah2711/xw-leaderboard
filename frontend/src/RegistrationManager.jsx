
import icon from "./icon.jpg";
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function RegistrationManager({setShowRegistrationManager, message, setMessage}) {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const { submitData, loading, error } = useSubmit("/api/register");

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password == confirmPassword) {
            const data = await submitData({email: email, password: password, username: username});
            console.log(data);
            if (data.success) {
                setShowRegistrationManager(false);
            }
            setMessage(data.message);
        } else {
            setMessage("Passwords don't match");
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
                            <label>Display Name:</label>
                            <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="off" className="form-control" placeholder="Display Name" required/>
                        </div>
                        <div className="row">
                            <div></div>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label htmlFor="email">Email Address:</label>
                            <input type="email" name="email" id="email" autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} className="form-control" placeholder="Enter email" required/>
                        </div>
                        <div className="row">
                            <div></div>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label htmlFor="password">Password:</label>
                            <input type="password" name="password" id="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} inputMode="text" autoCorrect="off" className="form-control" placeholder="Password" required/>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label htmlFor="password">Password:</label>
                            <input type="password" name="password" id="password" autoComplete="new-password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} inputMode="text" autoCorrect="off" className="form-control" placeholder="Password" required/>
                        </div>
                        <div className="row">
                            <p className="text-center text-danger">
                                {message} 
                            </p>
                        </div>
                        <button type="submit" className="btn btn-primary mx-2 mb-2" onClick={handleSubmit}>Submit</button>
                        <button type="submit" className="btn btn-secondary mx-2 mb-2" onClick={() => {setShowRegistrationManager(false); setMessage("")}}>Back</button>
                    </form>
                </div>
            <div className="col-4"></div>
            </div>
        </div>
    )
}