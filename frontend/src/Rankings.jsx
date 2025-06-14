import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);  // 1 hour = 3600 seconds
    const minutes = Math.floor((seconds % 3600) / 60);  // Remaining minutes
    const secs = seconds % 60;  // Remaining seconds

    if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}
const formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/New_York",
      year: "numeric", 
      month: "2-digit",   
      day: "2-digit",  
    });

export default function Rankings({day, kind}) {
    const {data, loading, error } = useFetch(`${"/api/sync/"}${formatter.format(day)}${'/'}${kind}`);
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    return (
        <div className="row d-flex justify-content-center align-items-center mb-4 mt-4">
            <div className="col-4"></div>
            <div className="col-4">
                <ul className="list-group list-group-flush">
                    {data.complete.map((entry, index) => (
                    <div key={index}>
                        <div className="d-flex align-items-center justify-content-center">
                            <h6 className="mb-0 me-2 lead">{index+1}.</h6>
                            <p className="mb-0 me-4 lead">{entry.username}</p>  
                            <p className="mb-0 ms-auto lead">{formatTime(entry.solve_time)}</p>
                        </div>
                        <hr className="col-md-12"></hr>
                    </div>
                    ))}
                    {data.incomplete.map((entry, index) => (
                    <div key={index}>
                        <div className="d-flex align-items-center text-center justify-content-center">
                            <p className="mb-0 me-2 lead">•</p>
                            <p className="mb-0 text-muted lead">{entry}</p>  
                            <p className="mb-0 ms-auto text-muted lead">-</p>
                        </div>
                        <hr className="col-md-12"></hr>
                    </div>
                    ))}
                </ul>
            </div>
            <div className="col-4"></div>
        </div>
    )
}