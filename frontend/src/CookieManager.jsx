import { useState, useEffect} from "react";
import CookieUpload from "./CookieUpload";
import CookieDeletion from "./CookieDeletion";
import { useFetch } from "./services/useFetch";
export default function CookieManager() {
    const { data, loading, error } = useFetch("/api/valid_cookie");
    const [validCookie, setValidCookie] = useState(false);

   useEffect(() => {
        if (data && data.success) {
            setValidCookie(data.is_valid);
        }
    }, [data]); 
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
 
    return (
        <div className="container">
            {!loading && (validCookie ? <CookieDeletion setValidCookie={setValidCookie}/> :  <CookieUpload setValidCookie={setValidCookie}/>)}
        </div>
    )
}