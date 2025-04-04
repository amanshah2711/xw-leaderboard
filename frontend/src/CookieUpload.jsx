import { useState } from "react";
import { useSubmit } from "./services/useSubmit";

export default function CookieUpload({setValidCookie}) {
    const [cookie, setCookie] = useState("");
    const { submitData, loading, error } = useSubmit("/api/store_cookie");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({nytCookie: cookie});
        if (data.success) {
            setValidCookie(data.success);
        } else {
            console.log(data.message);
        }
    };  
    return (
        <div className="container">
            <div className="row">
                <div className="col-4"></div>
                <div className="col-4">
                    Instructions to get your cookie <a href="https://xwstats.com/link" target="_blank">here</a>
                    <form>
                        <div className="form-group text-start mb-4">
                            <label>NYT-S Cookie:</label>
                            <input name="cookie" value={cookie} onChange={(e) => setCookie(e.target.value)} className="form-control" placeholder="NYT-S"/>
                        </div>
                        <button type="submit" className="btn btn-primary me-4" onClick={handleSubmit}>Submit</button>
                    </form>
                </div>
                <div className="col-4"></div>
            </div>
        </div>
    )
}
