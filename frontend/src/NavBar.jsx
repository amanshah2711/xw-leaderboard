import {Link, useLocation, useNavigate, useMatch} from "react-router-dom";
import Dropdown from 'react-bootstrap/Dropdown';

export default function NavBar(){
    const location = useLocation();
    const navigate = useNavigate();
    const isActive = (path) => location.pathname === path;
    const isResetPassword = useMatch('/reset-password/:token')
    const appear = location.pathname != '/' && location.pathname != '/forgot-password' && !isResetPassword;

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
              <div className="navbar-brand"><Link to="/" className='navbar-brand text-decoration-none'>XWLeaderboard</Link></div>
              {appear && <Link to='/mini' className={`nav-item ms-auto btn ${isActive('/mini') ? 'active' : ''}`}>Mini</Link>}
              {appear && <Link to='/daily' className={`nav-item btn ${isActive('/daily') ? 'active' : ''}`}>Daily</Link>}
              {appear && 
                    <Dropdown>
                        <Dropdown.Toggle as={Link} className={`nav-item btn ${(isActive('/nyt-settings') || isActive('/account-settings')) ? 'active' : ''}`} id="settings-dropdown">
                            Settings
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            <Dropdown.Item as={Link} to="/account-settings">
                            Account Settings
                            </Dropdown.Item>
                            <Dropdown.Item as={Link} to="/nyt-settings">
                            NYT Settings
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                    }
              {appear && <Link className="nav-item btn" id="logout" onClick={() => handleClick("logout")}>Logout</Link>}
          </nav>
      </div>
    <hr className="col-md-11"></hr>
  </div>
);
}




