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
        <p>Aquí tienes un vídeo que muestra las instrucciones para poder hacer reservas:</p>
        <div className="video-container">
          <iframe
            width="100%"
            height="600"
            src="https://www.youtube.com/embed/lIt-rLgV6P0?si=baX0TJRzPL-hhWbs?controls=1&autoplay=0&rel=0&modestbranding=1"
            title="Tutorial de YouTube"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
        
      </div>

      <Contacto />

    </div>
  );
};

export default Help;
