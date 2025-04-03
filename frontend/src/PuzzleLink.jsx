import { useEffect, useState } from "react";

export default function PuzzleLink({day}) {
    const [link, setLink] = useState("");
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${"/api/puzzle_link/"}${day.toISOString().substring(0,10)}`, {
                    method: 'GET',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                });
            
                const data = await response.json();
                setLink(data.puzzle_link);

            } catch (error) {
                console.error('Puzzle Link Retrieval Failed', error);
            }
        }
        fetchData()
    }, [])
    return (
        <div className="row">
            <a href={link} target="_blank" className="link-secondary">Link to Puzzle</a>
        </div>
    );
}