
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangePassword() {
    const [password, setPassword] = useState("");
    const { submitData, loading, error } = useSubmit("/api/change_password");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({password: password});
        if (data.success) {
            setPassword("");
        }
    }
    return (
        <div className="row justify-content-center m-4">
            <div></div>
            <div className="col-4">
                <form>
                    <div className="form-group text-start mb-4">
                        <label htmlFor="password">Password:</label>
                        <input type="password" name="password" id="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} inputMode="text" className="form-control" placeholder="Password"/>
                    </div>
                    <button type="submit" className="btn btn-primary me-4" onClick={handleSubmit}>Submit</button>
                </form>
            </div>
        </div>
    );
}