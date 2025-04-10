import ChangeEmail from "./ChangeEmail";
import ChangePassword from "./ChangePassword";
import ChangeUsername from "./ChangeUsername";
import CookieManager from "./CookieManager";
import DeleteAccount from "./DeleteAccount";

export default function Settings() {
    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center">
            <CookieManager/>
            <ChangeUsername/>
            <ChangeEmail/>
            <ChangePassword/>
            <DeleteAccount/>
        </div>
    )
}