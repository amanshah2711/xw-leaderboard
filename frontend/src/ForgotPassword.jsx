
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const { submitData, loading, error } = useSubmit("/api/request-reset-password");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({email: email});
        setMessage(data.message);
        console.log(data.debug);
    };  
    return (
        <div className="container">
            <h3>Password Reset</h3>
            <p>Enter your email, and we will send you a link that will give you instructions to reset your password.</p>
            <div className="row">
                <div className="col-4"></div>
                <div className="col-4">
                    <form onSubmit={handleSubmit}>
                        <input className="form-control" type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Enter your email" />
                        <button className="btn btn-primary m-4" type="submit">Send Reset Link</button>
                        <p className="text-secondary">{message}</p>
                    </form>
                </div>
            <div className="col-4"></div>

            </div>
        </div>
    );
}