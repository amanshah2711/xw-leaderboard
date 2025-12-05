import {Link, useLocation, useNavigate, useMatch} from "react-router-dom";
import Dropdown from 'react-bootstrap/Dropdown';
import Collapse from 'bootstrap/js/dist/collapse';
import { useRef, useEffect } from "react";
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
  const navbarRef = useRef(null);
  const bsCollapseRef = useRef(null);

  useEffect(() => {
    if (navbarRef.current) {
      bsCollapseRef.current = new Collapse(navbarRef.current, { toggle: false });
    }
  }, []);

  const closeNavbar = () => {
    if (bsCollapseRef.current && navbarRef.current.classList.contains('show')) {
      bsCollapseRef.current.hide();
    }
  };

  const toggleNavbar = () => {
  if (bsCollapseRef.current) {
    bsCollapseRef.current.toggle();
  }
};
  return (
    <div className="row justify-content-center mb-2">
      <div className="col-md-10">
          <div className="navbar navbar-expand-lg navbar-light d-flex">
              <div className="navbar-brand"><Link to="/" className='navbar-brand text-decoration-none'>XWLeaderboard</Link></div>
                    {
                    appear && 
                        <button
                            className="navbar-toggler"
                            type="button"
                            aria-controls="navbarNav"
                            aria-expanded={false}
                            aria-label="Toggle navigation"
                            onClick={toggleNavbar}
                        >                        
                            <span className="navbar-toggler-icon"></span>
                        </button>                    
                    }

               <div className="collapse navbar-collapse" id="navbarNav" ref={navbarRef}>
                    <ul className="navbar-nav ms-auto">
                        {appear && 
                            <li className="nav-item">
                                <Link to='/nyt-bonus' className={`ms-auto btn ${isActive('/nyt-bonus') ? 'active' : ''}`} onClick={closeNavbar}>Bonus</Link>
                            </li>
                        }
                        {appear && 
                            <li className="nav-item">
                                <Link to='/nyt-mini' className={`btn ${isActive('/nyt-mini') ? 'active' : ''}`}onClick={closeNavbar}>Mini</Link>
                            </li>
                        }
                        {appear && 
                            <li className="nav-item">
                                <Link to='/nyt-daily' className={`btn ${isActive('/nyt-daily') ? 'active' : ''}`}onClick={closeNavbar}>Daily</Link>
                            </li>
                        }
                            {appear && (
                                <li className="nav-item dropdown">
                                <a
                                    className={`dropdown-toggle btn border-0 ${
                                    isActive("/nyt-settings") || isActive("/account-settings")
                                        ? "active"
                                        : ""
                                    }`}
                                    href="#"
                                    id="settingsDropdown"
                                    role="button"
                                    data-bs-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                    Settings
                                </a>
                                <ul className="dropdown-menu" aria-labelledby="settingsDropdown">
                                    <li>
                                    <Link className="dropdown-item text-center" to="/account-settings"onClick={closeNavbar}>
                                        Account Settings
                                    </Link>
                                    </li>
                                    <li>
                                    <Link className="dropdown-item text-center" to="/nyt-settings"onClick={closeNavbar}>
                                        NYT Settings
                                    </Link>
                                    </li>
                                </ul>
                                </li>
                            )}

                        {appear && <Link className="nav-item btn" id="logout" onClick={() => handleClick("auth/logout")}>Logout</Link>}
                    </ul>
              </div>
          </div>
      </div>
    <hr className="col-md-11"></hr>
  </div>
);
}




