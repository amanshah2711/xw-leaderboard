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
            <div className="container">
                <div className="row justify-content-center m-4">
                    <div></div>
                    <div className="col-4">
                        <form>
                            <div className="form-group text-start mb-4">
                                <label>Change Display Name:</label>
                                <input value={username} onChange={(e) => setUsername(e.target.value)} className="form-control" autoComplete="off" placeholder="New Display Name"/>
                            </div>
                            <button type="submit" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                        </form>
                    </div>
                </div>
            </div>
    );
}