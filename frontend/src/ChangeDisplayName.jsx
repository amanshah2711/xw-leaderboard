import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangeDisplayName() {
    const [displayName, setDisplayName] = useState("");
    const [message, setMessage] = useState("");
    const { submitData, loading, error } = useSubmit("/api/auth/change-display-name");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({displayName: displayName});
        setMessage(data.message);
        if (data.success) {
            setDisplayName("");
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
                                <input value={displayName} onChange={(e) => setDisplayName(e.target.value)} className="form-control" autoComplete="off" placeholder="New Display Name"/>
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