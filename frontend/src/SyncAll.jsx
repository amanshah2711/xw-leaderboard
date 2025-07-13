import { useState } from "react";
import { useSubmit} from "./services/useSubmit";
import { useNavigate } from "react-router-dom";

export default function SyncAll() {
    const navigate = useNavigate();
    const { submitData: submitDaily, loading: loadingDaily, error: errorDaily } = useSubmit("/api/full-sync/daily");
    const { submitData: submitMini, loading: loadingMini, error: errorMini } = useSubmit("/api/full-sync/mini");
    const [message, setMessage] = useState("");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const [data, data2] = await Promise.all([submitDaily({}), submitMini({})]);
        setMessage(data.message + '\n' + data2.message);
    }
    return (
        <div className="row justify-content-center m-2">
            <div className="col-4">
                <div className="d-flex justify-content-center">
                    <button type="button" className="btn btn-info" onClick={handleSubmit} disabled={loadingDaily || loadingMini}>
                        Sync All NYT Data 
                    </button>
                </div>
            </div>
            {message && <p className="text-center text-secondary">{message}</p>}
        </div>
    )
}