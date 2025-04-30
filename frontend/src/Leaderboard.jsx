import { useState, useEffect } from "react"
import DayManager from "./DayManager"
import Rankings from "./Rankings"
import LinkManager from "./LinkManager";
import PuzzleLink from "./PuzzleLink";

export default function Leaderboard ({kind}) {
  const [day, setDay] = useState(new Date());
  console.log(day);
  console.log(day.toISOString());

  return (
      <div className="container-fluid">
          <DayManager day={day} setDay={setDay}/>
          <PuzzleLink day={day} kind={kind}/>
          <Rankings day={day} kind={kind}/>
          <LinkManager/>
      </div>
  )
}