import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";
import RankingsRow from "./RankingsRow";

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
            <div className="col-4 justify-content-center align-items-center">
                <ul className="list-group list-group-flush">
                    {data.complete.map((entry, index) => (
                        <div key={index}>
                            <RankingsRow entry={entry} rank={index} row_id={entry.id} current_id={data.current_user} completed={true}/> 
                            <hr className="col-md-12"></hr>
                        </div>
                    ))}
                    {data.incomplete.map((entry, index) => (
                        <div key={index}>
                            <RankingsRow entry={entry} rank={NaN} row_id={entry.id} current_id={data.current_user} completed={false}/> 
                            <hr className="col-md-12"></hr>
                        </div>
                    ))}
                </ul>
            </div>
            <div className="col-4"></div>
        </div>
    )
}