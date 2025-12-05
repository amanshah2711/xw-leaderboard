import { useState } from "react";
import { useSubmit} from "./services/useSubmit";
import { useNavigate } from "react-router-dom";

export default function SyncAll({source, variant}) {
    const navigate = useNavigate();
    const { submitData: submitDaily, loading: loadingDaily, error: errorDaily } = useSubmit("/api/puzzles/nyt/daily/sync-all");
    const { submitData: submitMini, loading: loadingMini, error: errorMini } = useSubmit("/api/puzzles/nyt/mini/sync-all");
    const { submitData: submitBonus, loading: loadingBonus, error: errorBonus} = useSubmit("/api/puzzles/nyt/bonus/sync-all");
    const [message, setMessage] = useState("");
    const handleSubmit = async (e) => {
        e.preventDefault();
        const [data, data2, data3] = await Promise.all([submitDaily({}), submitMini({}), submitBonus({})]);
        setMessage(data.message + '\n' + data2.message + '\n'+ data3.message);
    }
    return (
        <div className="row justify-content-center m-2">
            <div className="col-12 col-md-6">
                <div className="d-flex justify-content-center">
                    <button type="button" className="btn btn-info" onClick={handleSubmit} disabled={loadingDaily || loadingMini || loadingBonus}>
                        Sync All NYT Data 
                    </button>
                </div>
            </div>
            {message && <p className="text-center text-secondary">{message}</p>}
        </div>
    )
}