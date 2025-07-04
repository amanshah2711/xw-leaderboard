import CookieManager from "./CookieManager";
import SyncAll from "./SyncAll";

export default function NYTSettings() {
    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center">
            <CookieManager/>
            <SyncAll/>
        </div>
    )
}