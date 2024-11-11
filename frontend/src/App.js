import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import Footer from './components/layout/Footer';
import Navbar from './components/layout/Navbar';
import Home from './screens/Home';
import SportDetail from './screens/SportDetail';

function App() {
  return (
    <Router>
      <Navbar />
      
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/deportes/:sportName" element={<SportDetail />} />
        </Routes>
      </div>

      <Footer />
    </Router>
  );
}

export default App;
