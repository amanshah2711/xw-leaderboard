import { useSubmit} from "./services/useSubmit";
import { useNavigate } from "react-router-dom";

export default function SyncAll() {
    const navigate = useNavigate();
    const { submitData, loading, error } = useSubmit("/api/full-sync/daily");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({});
        if (data.message) {
            console.log(data.message)
        }
    }
    return (
        <div className="container">
            <div className="row justify-content-center m-2">
                <div className="col-4">
                    <div className="d-flex justify-content-center">
                        <button type="button" className="btn btn-info" onClick={handleSubmit} disabled={loading}>
                            Sync All NYT Data 
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}