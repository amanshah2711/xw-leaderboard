import ChangeDisplayName from "./ChangeDisplayName";
import ChangeEmail from "./ChangeEmail";
import ChangePassword from "./ChangePassword";
import DeleteAccount from "./DeleteAccount";

export default function AccountSettings() {
    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center">
            <ChangeDisplayName/>
            <ChangeEmail/>
            <ChangePassword/>
            <DeleteAccount/>
        </div>
    )
}