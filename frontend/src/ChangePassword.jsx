
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangePassword() {
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const { submitData, loading, error } = useSubmit("/api/change-password");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({password: password});
        setMessage(data.message);
        if (data.success) {
            setPassword("");
        } 
    }
    return (
        <div className="container">
            <div className="row justify-content-center m-2">
                <div className="col-4">
                    <form>
                        <div className="form-group text-start mb-4">
                            <label htmlFor="password">Change Password:</label>
                            <input type="password" name="password" id="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} inputMode="text" className="form-control" placeholder="New Password"/>
                        </div>
                        <div className="d-flex justify-content-center">
                            <button type="submit" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                        </div>
                    </form>
                </div>
            </div>
	    	<div className="row">
                <p className="text-center text-secondary">{message}</p>
            </div>
        </div>
    );
}