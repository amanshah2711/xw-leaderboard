
import { useSubmit } from "./services/useSubmit";
import { useNavigate } from "react-router-dom";

export default function DeleteAccount() {
    const navigate = useNavigate();
    const { submitData, loading, error } = useSubmit("/api/delete_account");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const confirmed = window.confirm("Are you sure you want to delete your account? This cannot be undone.");
        if (!confirmed) return;
        const data = await submitData({});
        if (data.success) {
            navigate('/')
        }
    }
    return (
        <div className="row justify-content-center m-4">
            <div className="col-4">
                <button type="button" className="btn btn-danger" onClick={handleSubmit} disabled={loading}>
                    Delete Account
                </button>
            </div>
        </div>
    )
}