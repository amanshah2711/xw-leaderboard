
export default function DayManager({day, setDay}) {
    const nyDate = new Date('1993-11-21T00:00:00-05:00'); // 00:00 represents midnight in New York (UTC-5)
    const nyDateOnly = new Date(nyDate.setHours(0, 0, 0, 0));

    const onClick = (shift) => {
        return (() => {
            const updatedDate = new Date(day);
            const currentDate = new Date().setHours(0,0,0,0);
            updatedDate.setDate(updatedDate.getDate() + shift);
            updatedDate.setHours(0,0,0,0);
            if (updatedDate <= currentDate && updatedDate >= nyDateOnly) {
                setDay(updatedDate);
            }
        }
    )
    };
    const formatter = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/New_York",
      weekday: "long", 
      year: "numeric", 
      month: "long",   
      day: "numeric",  
    });
    return (
            <div className="row justify-content-center align-items-center mb-5">
                    <button type="button" className="btn col-1 border-0" onClick={onClick(-1)}>←</button>
                    <p className="h2 mb-0 col-4 text-break">{formatter.format(day)}</p>
                    <button type="button" className="btn col-1 border-0" onClick={onClick(1)}>→</button>
            </div>
    )
}