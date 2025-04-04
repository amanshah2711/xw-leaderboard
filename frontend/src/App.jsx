import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Leaderboard from './Leaderboard';
import NavBar from './NavBar';
import CookieManager from './CookieManager';
import HomePage from './HomePage';
import Settings from './Settings';
import { useFetch } from './services/useFetch';

function App() {
    const { data, loading, error } = useFetch("/api/csrf_token");
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    if (data.csrf_token) {
      window.csrfToken = data.csrf_token
    }
  return (
    <Router>
      <NavBar/>
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/leaderboard" element={<Leaderboard/>}/>
        <Route path="/settings" element={<Settings/>}/>
        <Route path="/cookies" element={<CookieManager/>}/>
      </Routes>
    </Router>
  )
}

export default App
