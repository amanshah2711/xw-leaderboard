import CookieManager from "./CookieManager";
import ExportData from "./ExportData";
import SyncAll from "./SyncAll";

export default function NYTSettings() {
    return (
        <div className="container-fluid d-flex flex-column justify-content-center align-items-center">
            <CookieManager/>
            <SyncAll/>
            <ExportData source={'nyt'} variant={'daily'}/>
            <ExportData source={'nyt'} variant={'mini'}/>
            <ExportData source={'nyt'} variant={'bonus'}/>
        </div>
    )
}