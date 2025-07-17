import { useState, useEffect } from "react"
import DayManager from "./DayManager"
import Rankings from "./Rankings"
import LinkManager from "./LinkManager";
import PuzzleLink from "./PuzzleLink";
import DateSubtitle from "./DateSubtitle";
import { useFetch } from "./services/useFetch";

const formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/New_York",
      year: "numeric", 
      month: "2-digit",   
      day: "2-digit",  
    });

export default function Leaderboard ({kind}) {
  const [day, setDay] = useState(new Date());
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    fetch(`/api/sync/${formatter.format(day)}/${kind}/True`)
    .then(res => res.json())
    .then(() => {
      setTimeout(() => {
        setRefreshTrigger(prev => prev + 1);
      }, 50); 
    })
    .catch(err => console.error("Refresh failed:", err));
  };
  return (
      <div className="container-fluid d-flex flex-column justify-content-center">
          <DayManager day={day} setDay={setDay}/>
          <DateSubtitle day={day} kind={kind} handleClick={handleRefresh}/>
          <Rankings day={day} kind={kind} refreshTrigger={refreshTrigger}/>
          <LinkManager/>
      </div>
  )
}