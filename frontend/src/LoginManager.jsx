import { useNavigate } from "react-router-dom";
import icon from "./icon.jpg"
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function LoginManager ({setShowRegistrationManager, message, setMessage}) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const { submitData, loading, error } = useSubmit("/api/login");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({email: email, password: password});
        console.log(data);
        if (data.logged_in) {
            navigate(data.redirect);
        } else {
            setMessage(data.message);
        }
    };  

    return (
        <div>
            <div className="row justify-content-center">
                <img src={icon} className="img-fluid" style={{ maxWidth: "300px", height: "auto" }}></img>
            </div>
            <div className="row mb-2">
                <div className="col-4"></div>
                <div className="col-4 d-flex justify-content-center">
                    <form method="post" autoComplete="on" onSubmit={handleSubmit}>
                        <div className="text-start mb-4">
                            <input className="form-control" name="username" type="email" id="username" autoCorrect="off" autoCapitalize="off" autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required/>
                        </div>
                        <div className="row">
                        </div>
                        <div className="text-start mb-4">
                            <input className="form-control" name="password" type="password" id="password" autoCorrect="off" autoCapitalize="off" autoComplete="current-password"  value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required/>
                        </div>
                        <button type="submit" className="btn btn-primary mx-2 mb-2">Submit</button>
                        <button type="button" className="btn btn-secondary mx-2 mb-2" onClick={() => {setShowRegistrationManager(true);setMessage("")}}>Register</button>
                    </form>
                </div>
                <div className="col-4"></div>
            </div>
                <div className="row">
                    <p className="text-center text-secondary">
                        {message}
                    </p>
                </div>
        </div>
    )
}
