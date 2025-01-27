
export default function CookieDeletion({showDeletePage, setShowDeletePage}) {
    const handleSubmit = async (e) => {
        try {
            e.preventDefault();
            const response = await fetch('/api/remove_cookie', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            setShowDeletePage(false);
        } catch (error) {
            console.error("Storing cookie failed", error);
        }
    };  
    return (
        <div className="row justify-content-center">
            <div className="col-2"></div>
            <div className="col-8">
                <h3 className="display-6">Unlink NYT Account</h3>
                <p>Right now we have your NYT cookie safely encrypted so we can automatically insert your solve times. If you want to unlink your account, click the following button unlink account.</p>
                <button className="btn btn-danger" type="submit" onClick={handleSubmit}>Unlink Account</button>
            </div>
            <div className="col-2"></div>
        </div>
    )
}