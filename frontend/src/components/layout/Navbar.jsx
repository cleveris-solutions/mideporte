import { Link } from 'react-router-dom';

import './../../App.css';
import escudo from '../../assets/images/escudo_villanueva.webp';



const Navbar = () => {
  return (
    <nav className="navbar">
      
      <div className="navbar-logo">
        <div className="logo-image">
          <img src={escudo} alt="Escudo Villanueva de las Cruces" />
        </div>
        <Link to="/">Villanueva de las Cruces</Link>
      </div>
      
      <ul className="navbar-links">
        <li>
          <Link to="/reservas">Reservas</Link>
        </li>
        <li className="navbar-main-container">
          <Link to="/perfil">
            <span className="navbar-main-highlight">Perfil</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
};


export default Navbar;