import ChangeEmail from "./ChangeEmail";
import ChangePassword from "./ChangePassword";
import ChangeUsername from "./ChangeUsername";
import DeleteAccount from "./DeleteAccount";

export default function AccountSettings() {
    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center">
            <ChangeUsername/>
            <ChangeEmail/>
            <ChangePassword/>
            <DeleteAccount/>
        </div>
    )
}