import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Leaderboard from './Leaderboard';
import NavBar from './NavBar';
import CookieManager from './CookieManager';
import HomePage from './HomePage';
import { useFetch } from './services/useFetch';
import ForgotPassword from './ForgotPassword';
import ResetPassword from './ResetPassword';
import AccountSettings from './AccountSettings';
import NYTSettings from './NYTSettings';
import { RequireAuth } from './RequireAuth';


function App() {

 const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRefreshTrigger((prev) => prev + 1);
    }, 25 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const { data, loading, error } = useFetch("/api/security/csrf-token", [refreshTrigger]);

  useEffect(() => {
    if (data && data.csrf_token) {
      window.csrfToken = data.csrf_token;
    }
  }, [data]);

  if (loading) return <p>Loading...</p>;
  return (
    <Router>
      <NavBar/>
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/account-settings" element={<RequireAuth><AccountSettings/></RequireAuth>}/>
        <Route path="/nyt-daily" element={<RequireAuth><Leaderboard key='nyt-daily' source={'nyt'} variant={"daily"}/></RequireAuth>}/>
        <Route path="/nyt-mini" element={<RequireAuth><Leaderboard key='nyt-mini' source={'nyt'} variant={"mini"}/></RequireAuth>}/>
        <Route path="/nyt-bonus" element={<RequireAuth><Leaderboard key='nyt-bonus' source={'nyt'} variant={"bonus"}/></RequireAuth>}/>
        <Route path="/nyt-settings" element={<RequireAuth><NYTSettings/></RequireAuth>}/>
        <Route path="/forgot-password" element={<ForgotPassword/>}/>
        <Route path="/reset-password/:token" element={<ResetPassword/>}/>
      </Routes>
    </Router>
  )
}

export default App
