import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";

export default function PuzzleLink({day}) {
    day.setHours(0,0,0,0); // hack for dealing with daylight savings
    const { data, loading, error } = useFetch(`${"/api/puzzle_link/"}${day.toISOString().substring(0,10)}`);
    return (
        <div className="row">
            {!loading && <a href={data.puzzle_link} target="_blank" className="link-secondary">Link to Puzzle</a>}
        </div>
    );
}