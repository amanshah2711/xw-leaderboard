import { useState, useEffect } from "react"
import Rankings from "./Rankings"
import LinkManager from "./LinkManager";
import DateDisplay from "./DateDisplay";
import { useFetch } from "./services/useFetch";

const formatter = new Intl.DateTimeFormat("en-CA", {
      timeZone: "America/New_York",
      year: "numeric", 
      month: "2-digit",   
      day: "2-digit",  
    });

export default function Leaderboard ({source, variant}) {
  const [date, setDate] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const {data, loading, error } = useFetch(`/api/puzzles/${source}/${variant}/latest/date`);

  const handleRefresh = () => {
    fetch(`/api/puzzles/${source}/${variant}/${formatter.format(day)}/rankings?refresh=true`)
    .then(res => res.json())
    .then(() => {
      setTimeout(() => {
        setRefreshTrigger(prev => prev + 1);
      }, 50); 
    })
    .catch(err => console.error("Refresh failed:", err));
  };

  useEffect(() => {
    setDate(null);
    if (!loading && data?.date) {
      const [y, m, d] = data.date.split("-");
      setDate(new Date(y, m - 1, d));
    }
  }, [data, loading]);
  
  return (
      <div className="container-fluid d-flex flex-column justify-content-center">
          {date && <DateDisplay date={date} setDate={setDate} source={source} variant={variant} handleClick={handleRefresh}/>}
          {date && <Rankings date={date} source={source} variant={variant} refreshTrigger={refreshTrigger}/>}
          <LinkManager/>
      </div>
  )
}