import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './../../auth/AuthContext';


import './../../App.css';
import escudo from '../../assets/images/escudo_villanueva.webp';

const Navbar = () => {
  const { user } = useContext(AuthContext);

  return (
    <nav className="navbar">
      
      <div className="navbar-logo">
        <div className="logo-image">
          <img src={escudo} alt="Escudo Villanueva de las Cruces" />
        </div>
        <Link className="logo-text" to="/">
          <span className="line-break">Villanueva de</span>
          <span className="line-break">las Cruces</span>
        </Link>
      </div>

      {user ? (
        <>
          <ul className="navbar-links">
            <li>
              <Link to="/ayuda">Ayuda</Link>
            </li>
            <li>
              <Link to="/reservas">Mis reservas</Link>
            </li>
            <li>
              <Link to="/deportes">Deportes</Link>
            </li>
            <li className="navbar-main-container">
              <Link className='navbar-main-link' to="/perfil">
                <span className="navbar-main-highlight">Mi perfil</span>
              </Link>
            </li>
          </ul>
        </>
      ) : (
        <ul className="navbar-links">
          <li>
            <Link to="/ayuda">Ayuda</Link>
          </li>
          <li className="navbar-main-container">
            <Link className='navbar-main-link' to="/">
              <span className="navbar-main-highlight">Iniciar sesión</span>
            </Link>
          </li>
        </ul>
      )}
      
      
    </nav>
  );
};


export default Navbar;