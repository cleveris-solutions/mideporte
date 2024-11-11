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
        <li>
          <Link to="/perfil">Perfil</Link>
        </li>
        <li className="cart-container">
          <Link to="/cesta">
            <span className="cart-highlight">Cesta</span>
          </Link>
        </li>
      </ul>
    </nav>
  );
};


export default Navbar;