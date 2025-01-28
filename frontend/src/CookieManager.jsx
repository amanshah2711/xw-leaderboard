import { useState, useEffect} from "react";
import CookieUpload from "./CookieUpload";
import CookieDeletion from "./CookieDeletion";

export default function CookieManager() {
    const [cookie, setCookie] = useState("");
    const [showDeletePage, setShowDeletePage] = useState(false);
    const [isReady, setIsReady] = useState(false);

    useEffect (() => {
        const fillBoard = async () => {
          try {
              const response = await fetch("/api/valid_cookie", {
                  method: 'GET',
                  headers: {
                  'Content-Type': 'application/json',
                  },
              });
            const result = await response.json();
            setShowDeletePage(result);
            setIsReady(true);
          } catch (error) {
              console.error('Checking if you have a connected NYT account failed.', error);
          }
      }; 
      fillBoard()
      }, []);

    return (
        <div>
            {isReady && (showDeletePage ? <CookieDeletion showDeletePage={showDeletePage} setShowDeletePage={setShowDeletePage}/> :  <CookieUpload cookie={cookie} setCookie={setCookie} showDeletePage={showDeletePage} setShowDeletePage={setShowDeletePage}/>)}
        </div>
    )
}