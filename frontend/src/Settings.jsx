import ChangeUsername from "./ChangeUsername";
import CookieManager from "./CookieManager";

export default function Settings() {
    return (
        <div className="container-fluid justify-content-center align-items-center">
            <ChangeUsername/>
            <CookieManager/>
        </div>
    )
}