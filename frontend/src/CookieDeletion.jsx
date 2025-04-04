import { useSubmit } from "./services/useSubmit";

export default function CookieDeletion({setValidCookie}) {
    const { submitData, loading, error } = useSubmit("/api/remove_cookie");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = await submitData({});
        setValidCookie(!data.success);
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