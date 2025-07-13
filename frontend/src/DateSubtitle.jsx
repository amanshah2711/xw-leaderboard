import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";
import { RotateCcw } from "lucide-react";
import PuzzleLink from "./PuzzleLink";
import RefreshDate from "./RefreshDate";

const formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/New_York",
      year: "numeric", 
      month: "2-digit",   
      day: "2-digit",  
    });

export default function DateSubtitle({day, kind, handleClick}) {
    return (
        <div className="d-flex justify-content-center align-items-center">
                <PuzzleLink day={day} kind={kind}/>
                <RefreshDate onRefresh={handleClick}/>
        </div>
    );
}