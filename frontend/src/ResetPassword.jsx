
import { useState } from 'react';
import {useParams} from 'react-router-dom';
import { useSubmit } from './services/useSubmit';

export default function ResetPassword() {
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [message, setMessage] = useState("");

    const { token } = useParams();
    const { submitData, loading, error } = useSubmit(`/api/auth/reset-password/${token}`);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password == confirmPassword) {
            const data = await submitData({password: password});
            console.log(data);
            setMessage(data.message);
        } else {
            setMessage("Passwords don't match");
        }
    };  
    console.log(token);
    return (
        <div className="container">
            <h3>Reset Password</h3>
            <div className="row justify-content-center m-2">
                <div></div>
                <div className="col-4">
                    <form>
                        <div className="form-group text-start mb-4">
                            <label htmlFor="password">Password:</label>
                            <input type="password" name="password" id="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} inputMode="text" autoCorrect="off" className="form-control" placeholder="Password" required/>
                        </div>
                        <div className="form-group text-start mb-4">
                            <label htmlFor="password">Confirm Password:</label>
                            <input type="password" name="password" id="password" autoComplete="new-password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} inputMode="text" autoCorrect="off" className="form-control" placeholder="Confirm Password" required/>
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