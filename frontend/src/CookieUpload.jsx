
export default function CookieUpload({cookie, setCookie, showDeletePage, setShowDeletePage}) {
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/store_cookie', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({nytCookie: cookie})
            });
            const data = await response.json();
            if (response.status == 400) {
                alert("Your submitted cookie appears invalid. Double check you copied your cookie correctly.")
            } else {
                setShowDeletePage(true);
            }
        } catch (error) {
            console.error("Storing cookie failed", error);
        }
    };  
    return (
        <div className="container">
            <div className="row">
                <div className="col-4"></div>
                <div className="col-4">
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
            <div className="row">
                <h3>Step 1: Log in to your NY Times Games Account on their <a href="https://www.nytimes.com/crosswords">website</a></h3>
                <h3>Step 2: Access your cookie using developer tools</h3>
                    <p>On Google Chrome, go to settings &rarr; more tools &rarr; developer tools.</p>
                    <p>Then find the Application tab and under storage there will be a Cookies section. In the Cookies section there will be a link to NYTimes, select that and copy the value attached to the NYT-S cookie.</p>
                <h3>Step 3: Type "NYT-S=value_copied_from_step_2" into the above text box, and submit. </h3>
            </div>
        </div>
    )
}
