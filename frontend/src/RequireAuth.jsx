import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useFetch } from "./services/useFetch";

export function RequireAuth({ children }) {
  const navigate = useNavigate();
  const { data, loading, error } = useFetch("/api/auth/check-login");

  useEffect(() => {
    if (loading) return;
    if (error || !data?.logged_in) {
      navigate("/");
    }
  }, [loading, error, data, navigate]);

  if (loading) return <p>Loading...</p>;

  return children;
}