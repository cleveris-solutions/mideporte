import React from 'react';
import './../../assets/styles/components/layout/Contacto.css';

const Contacto = () => {
  return (
    <div className="contact-info">
      <h2>Contacto del Ayuntamiento</h2>
      <p>Si tienes algún problema con tus reservas o necesitas asistencia, no dudes en contactarnos o en visitarnos:</p>
        <div className="contact-details">
          <ul>
            <li><strong>Dirección:</strong> Calle Constitucion, 2, 21592 Villanueva de las Cruces, Huelva</li>
            <li><strong>Teléfono:</strong> 959 57 80 01</li>
            <li><strong>Correo electrónico:</strong> ayto@villanuevadelascruces.es</li>
            <li><strong>Horario:</strong> Lunes a Viernes de 8:00 a 14:00</li>
          </ul>
        <div className="map-container">
          <iframe
            title="Mapa Villanueva de las Cruces"
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d197.49464765579268!2d-7.0244664840624385!3d37.62770215759442!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd11adc695476147%3A0xcdf413a8d4503fcc!2sAyuntamiento%20De%20Villanueva%20De%20Las%20Cruces!5e0!3m2!1ses!2ses!4v1732655979130!5m2!1ses!2ses"
            width="100%"
            height="300"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
          ></iframe>
        </div>
      </div>
    </div>
  );
};

export default Contacto;
