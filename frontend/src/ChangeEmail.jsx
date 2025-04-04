
import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function ChangeEmail() {
    const [email, setEmail] = useState("");
    const { submitData, loading, error } = useSubmit("/api/change_email");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({email: email});
        if (data.success) {
            setEmail("");
        }
    }
    return (
        <div className="row justify-content-center">
            <div></div>
            <div className="col-4">
                <form>
                    <div className="form-group text-start mb-4">
                        <label>Change Email:</label>
                        <input name="email" value={email} onChange={(e) => setEmail(e.target.value)} className="form-control" placeholder="New email"/>
                    </div>
                    <button type="submit" className="btn btn-primary me-4" onClick={handleSubmit}>Submit</button>
                </form>
            </div>
        </div>
    );
}