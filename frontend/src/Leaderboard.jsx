import { useState, useEffect } from "react"
import DayManager from "./DayManager"
import Rankings from "./Rankings"
import LinkManager from "./LinkManager";

export default function Leaderboard () {
  const [day, setDay] = useState(new Date());

  return (
      <div className="container-fluid">
          <DayManager day={day} setDay={setDay}/>
          <Rankings day={day}/>
          <LinkManager/>
      </div>
  )
}