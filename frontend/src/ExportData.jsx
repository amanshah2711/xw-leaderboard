import { useState } from "react";
import { useSubmit} from "./services/useSubmit";
import { useNavigate } from "react-router-dom";

export default function ExportData({kind}) {
    const navigate = useNavigate();
    const { submitData, loading, error } = useSubmit(`${"/api/export-data/"}${kind}`);
    const [message, setMessage] = useState("");
    const handleDownload = () => {
        window.open(`${"/api/export-data/"}${kind}`, '_blank');
    };
    const name = kind == 'daily' ? 'Daily' : 'Mini'
    return (
        <div className="row justify-content-center m-2">
            <div className="col-4">
                <div className="d-flex justify-content-center">
                    <button type="button" className="btn btn-info" onClick={handleDownload} disabled={loading}>
                        Export {name} Crossword Data 
                    </button>
                </div>
            </div>
            {message && <p className="text-center text-secondary">{message}</p>}
        </div>
    )
}