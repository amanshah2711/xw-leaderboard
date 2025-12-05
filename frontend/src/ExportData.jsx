import { useState } from "react";
import { useSubmit} from "./services/useSubmit";
import { useNavigate } from "react-router-dom";

export default function ExportData({source, variant}) {
    const { submitData, loading, error } = useSubmit(`/api/puzzles/${source}/${variant}/puzzle-history`);
    const [message, setMessage] = useState("");
    const handleDownload = () => {
        window.open(`/api/puzzles/${source}/${variant}/puzzle-history`, '_blank');
    };
    return (
        <div className="row justify-content-center m-2">
            <div className="col-4">
                <div className="d-flex justify-content-center">
                    <button type="button" className="btn btn-info" onClick={handleDownload} disabled={loading}>
                        Export {source.toUpperCase() + ' ' + variant.charAt(0).toUpperCase() + variant.slice(1)} Crossword Data 
                    </button>
                </div>
            </div>
            {message && <p className="text-center text-secondary">{message}</p>}
        </div>
    )
}