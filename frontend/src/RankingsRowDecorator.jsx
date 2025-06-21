
export default function RankingsRowDecorator({completed, rank}) {
    if (completed) {
        return (
            <div className="mb-0 me-2 lead" style={{ width: "2em", textAlign: "right" }}>
            {   
                rank === 0 ? '🥇' :
                rank === 1 ? '🥈' :
                rank === 2 ? '🥉' :
                `${rank + 1}.`
            }
            </div>
        );
    } else {
        return <p className="mb-0 me-2 lead">•</p>
    }
    

}