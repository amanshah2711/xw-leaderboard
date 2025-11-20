import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangeUsername() {
    const [username, setUsername] = useState("");
    const [message, setMessage] = useState("");
    const { submitData, loading, error } = useSubmit("/api/change-username");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({username: username});
        setMessage(data.message);
        if (data.success) {
            setUsername("");
        }
    }
    return (
            <div className="container">
                <div className="row justify-content-center m-2">
                    <div></div>
                    <div className="col-8 col-md-4">
                        <form>
                            <div className="form-group text-start mb-4">
                                <label>Change Display Name:</label>
                                <input value={username} onChange={(e) => setUsername(e.target.value)} className="form-control" autoComplete="off" placeholder="New Display Name"/>
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