
import { useState, useEffect } from "react";
import { useFetch } from "./services/useFetch";
import PuzzleLink from "./PuzzleLink";
import RefreshDate from "./RefreshDate";

export default function DateDisplay({date, setDate, source, variant, handleClick}) {
    const { data, error, loading } = useFetch(`/api/puzzles/${source}/${variant}/${date.toISOString().substring(0, 10)}/metadata`);
    const [prevDate, setPrevDate] = useState(null);
    const [nextDate, setNextDate] = useState(null);
    const formatter = new Intl.DateTimeFormat("en-US", {
      weekday: "long", 
      year: "numeric", 
      month: "long",   
      day: "numeric",  
    });
    const onClick = (shift) => {
        return (()=> {
            if (shift == 1) {
                setDate(nextDate)
            } else if (shift == -1) {
                setDate(prevDate)
            }
        })
    }
    useEffect(() => {
        if (data && data.exists) {
            const prevParts = data.prev_date.split('-');
            const nextParts = data.next_date.split('-');
            setPrevDate(new Date(prevParts[0], prevParts[1]-1, prevParts[2]));
            setNextDate(new Date(nextParts[0], nextParts[1]-1, nextParts[2]));
        } else {
            setPrevDate(null);
            setNextDate(null);
        }
    }, [data]); 
    return (
        <div className="container">
            <div className="row justify-content-center align-items-center mb-2">
                <div className="col-4 d-flex justify-content-end">
                    <button type="button" className="btn border-0" onClick={onClick(-1)}>←</button>
                </div>
                <div className="col-4 d-flex justify-content-center align-items-center">
                    <p className="h2 mb-0">{formatter.format(date)}</p>
                </div>
                <div className="col-4 d-flex justify-content-start">
                    <button type="button" className="btn border-0" onClick={onClick(1)}>→</button>
                </div>
            </div>
            <div className="d-flex justify-content-center align-items-center">
                    <PuzzleLink date={date} source={source} variant={variant}/>
                    <RefreshDate onRefresh={handleClick}/>
            </div>
        </div>
    )
}