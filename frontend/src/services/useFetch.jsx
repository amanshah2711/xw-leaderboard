
import { useState, useEffect } from "react";
export function useFetch(endpoint, deps=[]) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
          if (!endpoint) {
            setData(null);
            setError(null);
            setLoading(false);
            return;
        }
        const fetchData = async () => {
          try {
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error("Failed to fetch");
            const result = await response.json();
            setData(result);
          } catch (err) {
            setError(err.message);
          } finally {
            setLoading(false);
          }
        };
    
        fetchData();
      }, [endpoint, ...deps]);
    
      return { data, loading, error };
    
}