import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import Footer from './components/layout/Footer';
import Navbar from './components/layout/Navbar';
import Home from './screens/Home';
import SportDetail from './screens/SportDetail';
import Login from './screens/Login';
import BookingsList from './screens/BookingsList';
import { useContext } from 'react';
import { AuthContext } from './auth/AuthContext'; 

function App() {
  const { user } = useContext(AuthContext);

  console.log(user);
  
  return (
    <Router>
      <Navbar />

      {user ? (
        <>
          <div className="content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/deportes/:sportName" element={<SportDetail />} />
              <Route path="/reservas" element={<BookingsList />} />
            </Routes>
          </div>
        </>
      ) : (
        <Routes>
          <Route path="*" element={<Login />} />
        </Routes>
      )}
      <Footer />
    </Router>
  );
}

export default App;
