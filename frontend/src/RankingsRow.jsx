
import{ useState, useEffect } from "react";
import { useSubmit } from "./services/useSubmit";
import RankingsRowDecorator from "./RankingsRowDecorator";
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);  // 1 hour = 3600 seconds
    const minutes = Math.floor((seconds % 3600) / 60);  // Remaining minutes
    const secs = seconds % 60;  // Remaining seconds

    if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

export default function RankingsRow({entry, row_id, rank, current_id, completed}) {
    const [hover, setHover] = useState(false);
    const [newName, setNewName] = useState("");
    const { submitData : submitUsername, loading : usernameLoading , error : usernameError } = useSubmit("/api/change-username");
    const { submitData : submitFriendRemoval, loading: friendRemovalLoading, error: friendRemovalError } = useSubmit("/api/remove-friend");

    const isSelf = current_id == row_id;
    const handleChange = async (e) => {
        e.preventDefault();
        const data = await submitUsername({'username' : newName});
        alert(data.message)
    };  

    const handleRemove = async (e) => {
        e.preventDefault();
        const data = await submitFriendRemoval({'friend_one' : current_id, 'friend_two' : row_id});
        alert(data.message);
    };  
    useEffect(() => {
        setNewName(entry.username);
    }, [entry.username]);
    return (
        <div 
            className="d-flex align-items-center justify-content-center"
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            <RankingsRowDecorator completed={completed} rank={rank} />
            
            {isSelf ? (
                <input
                    type="text"
                    className="mb-0 text-muted lead border-0 p-0"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') handleChange(e);
                    }}
                    autoFocus
                    style={{
                        outline: 'none',
                        whiteSpace: 'nowrap',
                    }}
                    size={newName.length+1}
                />
            ) : (
                <p
                    className={`mb-0 text-muted lead ${hover && isSelf ? 'cursor-pointer' : ''}`}
                    onClick={() => isSelf }
                >
                    {entry.username}
                </p>
            )}

            {completed ? 
            <div className="mb-0 ms-auto lead">{formatTime(entry.solve_time)}</div> :
            <p className="mb-0 ms-auto text-muted lead">-</p>

            }

            {hover && !isSelf && (
                <button
                    onClick={handleRemove}
                    className="btn btn-sm btn-outline-danger ms-3"
                    title="Remove friend"
                >
                    ×
                </button>
            )}
        </div>
    );
}
