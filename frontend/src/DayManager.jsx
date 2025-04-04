
export default function DayManager({day, setDay}) {
    const nyDate = new Date('1993-11-21T00:00:00-04:00'); // 00:00 represents midnight in New York (UTC-5)
    const nyDateOnly = new Date(nyDate.setHours(0, 0, 0, 0));

    const onClick = (shift) => {
        return (() => {
            const inspectedDate = new Date(day);
            const currentDate = new Date();
            const upperDate = new Date();
            inspectedDate.setDate(inspectedDate.getDate() + shift);
            inspectedDate.setHours(0,0,0,0);
            if (currentDate.getDay() == 0 || currentDate.getDay() == 6) {
                if (currentDate.getHours() >= 18) {
                    upperDate.setDate(upperDate.getDate() + 1);
                } 
            } else {
                if (currentDate.getHours() >= 22) {
                    upperDate.setDate(upperDate.getDate() + 1);
                }             
            }
            if (inspectedDate <= upperDate && inspectedDate >= nyDateOnly) {
                setDay(inspectedDate);
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
            <div className="row justify-content-center align-items-center mb-2">
                <div className="col-4 d-flex justify-content-end">
                    <button type="button" className="btn border-0" onClick={onClick(-1)}>←</button>
                </div>
                <div className="col-4 d-flex justify-content-center align-items-center">
                    <p className="h2 mb-0">{formatter.format(day)}</p>
                </div>
                <div className="col-4 d-flex justify-content-start">
                    <button type="button" className="btn border-0" onClick={onClick(1)}>→</button>
                </div>
            </div>
    )
}