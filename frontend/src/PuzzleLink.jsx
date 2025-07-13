import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";
import { RotateCcw } from "lucide-react";

export default function PuzzleLink({day, kind}) {
    day.setHours(0,0,0,0); // hack for dealing with daylight savings
    const { data, loading, error } = useFetch(`${"/api/puzzle-link/"}${day.toISOString().substring(0,10)}${'/'}${kind}`);
    return !loading && <a href={data.puzzle_link} target="_blank" className="link-secondary m-2">Link to Puzzle</a>
}