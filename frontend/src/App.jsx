import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Leaderboard from './Leaderboard';
import NavBar from './NavBar';
import CookieManager from './CookieManager';
import HomePage from './HomePage';
import Settings from './Settings';

function App() {
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
