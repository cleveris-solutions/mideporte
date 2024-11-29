import { useContext } from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import { AuthContext } from './auth/AuthContext';
import Footer from './components/layout/Footer';
import Navbar from './components/layout/Navbar';
import BookingsList from './screens/BookingsList';
import Home from './screens/Home';
import Login from './screens/Login';
import SportDetail from './screens/SportDetail';
import Profile from './screens/Profile';
import Help from './screens/Help';

function App() {
  const { user } = useContext(AuthContext);

  return (
    <Router>
      <Navbar />

      {user ? (
        <>
          <div className="content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/deportes" element={<Home />} />
              <Route path="/deportes/:sportName" element={<SportDetail />} />
              <Route path="/reservas" element={<BookingsList />} />
              <Route path="/ayuda" element={<Help />} />
              <Route path="/perfil" element={<Profile />} />
            </Routes>
          </div>
        </>
      ) : (
        <Routes>
          <Route path="*" element={<Login />} />
          <Route path="/ayuda" element={<Help />} />
        </Routes>
      )}
      <Footer />
    </Router>
  );
}

export default App;
