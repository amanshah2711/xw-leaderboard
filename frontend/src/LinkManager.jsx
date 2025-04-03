import { useEffect, useState } from "react";

export default function LinkManager() {
    const [link, setLink] = useState("");
    const handleCopyLink = () => {
        navigator.clipboard.writeText(link).then(() => {
            alert("Happy Sharing With Your Friends!");
            }).catch((err) => {
            console.error("Failed to copy link: ", err);
        });
    }
    const handleClick = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/reset_invite', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
            });
        
            const data = await response.json();
            setLink(`${window.location.origin}${data.invite}`);

        } catch (error) {
            console.error('Error while resetting your invite link', error);
        }
    };  

    useEffect (() => {
        const checkLogin = async () => {
        try {
            const response = await fetch('/api/get_invite', {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });
        
            const data = await response.json();
            setLink(`${window.location.origin}${data.invite}`);

        } catch (error) {
            console.error('Invite Link Retrieval Failed', error);
        }
    }; 
    checkLogin()
    }, []);
    return (
        <div className="flex align-items-center">
            <div className="mb-2">
                <button className="btn btn-primary mx-2 mb-2" onClick={handleCopyLink}>Copy Invite Link</button>
                <button className="btn btn-primary mx-2 mb-2" onClick={handleClick}>Reset Invite Link</button>
            </div>
            <div className="row">
                <div className="col-2"></div>
                <div className="col-8">
                    <p className="fw-bold" htmlFor="inviteLink">Your Invite Link:</p>
                    <p className="font-monospace overflow-auto text-wrap">{link}</p>
                </div>
                <div className="col-2"></div>
            </div>
        </div>
    )
}