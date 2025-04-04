import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangeUsername() {
    const [username, setUsername] = useState("");
    const { submitData, loading, error } = useSubmit("/api/change_username");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({username: username});
        if (data.success) {
            setUsername("");
        }
    }
    return (
        <div className="row justify-content-center">
            <div></div>
            <div className="col-4">
                <form>
                    <div className="form-group text-start mb-4">
                        <label>Change Username:</label>
                        <input name="username" value={username} onChange={(e) => setUsername(e.target.value)} className="form-control" placeholder="New Username"/>
                    </div>
                    <button type="submit" className="btn btn-primary me-4" onClick={handleSubmit}>Submit</button>
                </form>
            </div>
        </div>
    );
}