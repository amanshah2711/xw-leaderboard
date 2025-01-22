import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import Login from './Login';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='container'>
        <Login/>
    </div>
  )
}

export default App
