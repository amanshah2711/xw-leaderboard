
import { useEffect, useState } from 'react';

export default function useCsrf() {
  const [csrfToken, setCsrfToken] = useState(null);

  useEffect(() => {
    fetch('/api/security/csrf-token', {
      credentials: 'include', // important to include cookies
    })
      .then(res => res.json())
      .then(data => {
        setCsrfToken(data.csrf_token);
      });
  }, []);

  return csrfToken;
}