
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangeEmail() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const { submitData, loading, error } = useSubmit("/api/change_email");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({email: email});
        console.log(data);
        if (data.success) {
            setEmail("");
        }
        setMessage(data.message);
    }
    return (
        <div className="container">
            <div className="row justify-content-center m-2">
                <div className="col-4">
                    <form>
                        <div className="form-group text-start mb-4">
                            <label>Change Email:</label>
                            <input name="username" value={email} onChange={(e) => setEmail(e.target.value)} className="form-control" autoComplete="off" placeholder="New email"/>
                        </div>
                        <div className="d-flex justify-content-center">
                            <button type="submit" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                        </div>
                        <p className="text-secondary m-2">{message}</p>
                    </form>
                </div>
            </div>
        </div>
    );
}