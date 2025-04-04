
export default function CookieInstructions() {
    return (
        <div className="row">
            <h3>Step 1: Log in to your NY Times Games Account on their <a href="https://www.nytimes.com/crosswords">website</a></h3>
            <h3>Step 2: Access your cookie using developer tools</h3>
                <p>On Google Chrome, go to settings &rarr; more tools &rarr; developer tools.</p>
                <p>Then find the Application tab and under storage there will be a Cookies section. In the Cookies section there will be a link to NYTimes, select that and copy the value attached to the NYT-S cookie.</p>
            <h3>Step 3: Type "NYT-S=value_copied_from_step_2" into the above text box, and submit. </h3>
        </div>
    );
}