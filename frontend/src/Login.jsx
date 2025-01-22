import icon from "./icon.jpg"

export default function Login () {
    return (
        <div>
            <div className="row justify-content-center">
                <img src={icon} className="img-fluid" style={{ maxWidth: "300px", height: "auto" }}></img>
            </div>
            <div className="row">
                <form>
                    <div className="form-group text-start mb-4">
                        <label for="exampleInputEmail1">Email address:</label>
                        <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email"/>
                    </div>
                    <div className="row">
                        <div></div>
                    </div>
                    <div className="form-group text-start mb-4">
                        <label for="exampleInputPassword1">Password:</label>
                        <input type="password" className="form-control" id="exampleInputPassword1" placeholder="Password"/>
                    </div>
                    <button type="submit"className="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    )
}