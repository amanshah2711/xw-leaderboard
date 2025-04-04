import { useState, useEffect } from "react"
import DayManager from "./DayManager"
import Rankings from "./Rankings"
import LinkManager from "./LinkManager";
import PuzzleLink from "./PuzzleLink";

export default function Leaderboard () {
  const [day, setDay] = useState(new Date());
  console.log(day);
  console.log(day.toISOString());

  return (
      <div className="container-fluid">
          <DayManager day={day} setDay={setDay}/>
          <PuzzleLink day={day}/>
          <Rankings day={day}/>
          <LinkManager/>
      </div>
  )
}