import React from 'react';
import Contacto from '../components/layout/Contacto';
import './../assets/styles/screens/Help.css';

const Help = () => {
    
  return (
    <div className="help-container">
      <header className="help-header">
        <h1>Ayuda</h1>
        <p>Encuentra toda la información que necesitas aquí.</p>
      </header>

      <div className="help-manual">
        <h2>Manual de Usuario - ¿Cómo usar MiDeporte?</h2>
        <p>Estamos trabajando en un manual detallado. Próximamente estará disponible aquí.</p>
        <button className="download-button" disabled>
          Ver Manual de Usuario
        </button>
      </div>

      <Contacto />

    </div>
  );
};

export default Help;
