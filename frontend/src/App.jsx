import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import Login from './Login';
import Leaderboard from './Leaderboard';
import Register from './Register';

function App() {
  const [info, setInfo] = useState({
    email : "potato@gmail.com",
    password: "",
    data: null,
    success: false,
    registration: false,
    message: "" 
  })
  const handleChange = (newInfo) => {
   
    setInfo((prevInfo) => ({
      ...prevInfo, 
      ...newInfo
    }));
  }; 
  return (
    <div className='container'>
        {info.registration ? <Register info={info} update={handleChange}/> : (info.success ?  <Leaderboard/> : <Login info={info} update={handleChange}/>) }
    </div>
  )
}

export default App
