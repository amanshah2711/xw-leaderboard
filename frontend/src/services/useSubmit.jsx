
import { useState } from "react";

export function useSubmit(url, method = "POST") {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
  
    const submitData = async (body) => {
      setLoading(true);
      setError(null);
  
      try {
        const response = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
  
        if (!response.ok) throw new Error("Failed to submit");
  
        return await response.json();
      } catch (err) {
        setError(err.message);
        console.log(err.message);
      } finally {
        setLoading(false);
      }
    };
  
    return { submitData, loading, error };
  };
  