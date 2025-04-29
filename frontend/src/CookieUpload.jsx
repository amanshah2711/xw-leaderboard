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
            <div className="row justify-content-center m-2">
                <p>
                    Instructions to get your cookie <a href="https://xwstats.com/link" target="_blank">here</a>
                </p>

                <div className="col-4">
                    <form>
                        <div className="form-group text-start mb-4">
                            <label>NYT-S Cookie:</label>
                            <input name="cookie" value={cookie} onChange={(e) => setCookie(e.target.value)} className="form-control" placeholder="NYT-S"/>
                        </div>

                        <div className="d-flex justify-content-center">
                            <button type="submit" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                        </div>
                    </form>
                </div>
            </div>
    )
}
