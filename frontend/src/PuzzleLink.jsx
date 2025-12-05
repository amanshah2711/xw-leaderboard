import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";
import { RotateCcw } from "lucide-react";

export default function PuzzleLink({date, source, variant}) {
    date.setHours(0,0,0,0); // hack for dealing with daylight savings
    const { data, loading, error } = useFetch(`/api/puzzles/${source}/${variant}/${date.toISOString().substring(0,10)}/puzzle-link`);
    return !loading && <a href={data.puzzle_link} target="_blank" className="link-secondary m-2">Link to Puzzle</a>
}