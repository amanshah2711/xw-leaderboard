import { useEffect, useState } from "react";
import { useFetch } from "./services/useFetch";
import { useSubmit } from "./services/useSubmit";
export default function LinkManager() {
    const [link, setLink] = useState("");
    const { submitData, loading1, error1 } = useSubmit("/api/reset_invite");
    const { data, loading, error } = useFetch("/api/get_invite");
    useEffect(()=>{
        if (data && data.success) {
            setLink(`${window.location.origin}${data.invite}`);
        }
    }, [data])
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({});
        if (data.success) {
            setLink(`${window.location.origin}${data.invite}`);
        }
        
    };  
    const handleCopyLink = () => {
        navigator.clipboard.writeText(link).then(() => {
            alert("Happy Sharing With Your Friends!");
            }).catch((err) => {
            console.error("Failed to copy link: ", err);
        });
    }
    return (
        <div className="flex align-items-center">
            <div className="mb-2">
                <button className="btn btn-primary mx-2 mb-2" onClick={handleCopyLink}>Copy Invite Link</button>
                <button className="btn btn-primary mx-2 mb-2" onClick={handleSubmit}>Reset Invite Link</button>
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