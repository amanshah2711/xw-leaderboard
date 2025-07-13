import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";
import { RotateCcw } from "lucide-react";
import PuzzleLink from "./PuzzleLink";

export default function RefreshDate({onRefresh}) {
  return (
      <button
        onClick={onRefresh}
        className="btn btn-link p-0 m-0"
        aria-label="Refresh"
        style={{ lineHeight: 0 }}
      >
        <RotateCcw size={20} />
      </button>
  );
}