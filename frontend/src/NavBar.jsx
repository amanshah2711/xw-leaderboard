import {Link, useLocation, useNavigate} from "react-router-dom";

export default function NavBar(){
    const location = useLocation();
    const navigate = useNavigate();
    const isActive = (path) => location.pathname === path;

    const handleClick = async (id) => {
        try {
            await fetch(`/api/${id}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
            });
            navigate('/');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };  
  return (
    <div className="row justify-content-md-center d-flex mb-2">
      <div className="col-md-10">
          <nav className="navbar navbar-expand-lg navbar-light d-flex">
              <div className="navbar-brand">XWLeaderboard</div>
              {location.pathname != '/' && <Link to='/mini' className={`nav-item ms-auto btn ${isActive('/mini') ? 'active' : ''}`}>Mini</Link>}
              {location.pathname != '/' && <Link to='/daily' className={`nav-item btn ${isActive('/daily') ? 'active' : ''}`}>Daily</Link>}
              {location.pathname != '/' && <Link to='/settings' className={`nav-item btn ${isActive('/settings') ? 'active' : ''}`}>Settings</Link>}
              {location.pathname != '/' && <Link className="nav-item btn" id="logout" onClick={() => handleClick("logout")}>Logout</Link>}
          </nav>
      </div>
    <hr className="col-md-11"></hr>
  </div>
);
}




