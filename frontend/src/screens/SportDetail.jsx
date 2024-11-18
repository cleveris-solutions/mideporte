import { Calendar } from 'primereact/calendar';
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import Schedule from '../components/Schedule';
import SportCard from '../components/SportCard';
import { sportImages } from './../utils/imageMapping';

import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.min.css';
import 'primereact/resources/themes/saga-blue/theme.css';
import './../assets/styles/screens/SportDetail.css';

const SportDetail = () => {
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedSchedule, setSelectedSchedule] = useState(null);
    const [selectedLane, setSelectedLane] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [error, setError] = useState('');
    
    const { sportName } = useParams();
    
    // TODO: Fetch data from API with the sport name
    const sport = {sportName: sportName, description: 'Pista para 4 personas', message: null};

    // Not implemented yet. Need some backend logic to realize how its gonna work
    const handleBook = () => {
        console.log('Booked');
    }

    return (
        
        <div className="sport-detail-container">
            <div className="card-section">
                <SportCard 
                    sport={sport.sportName} 
                    description={sport.description} 
                    message={sport.message} 
                    image={sportImages[sport.sportName]} 
                />
            </div>
            <div className="info-section">
                <div className="sport-header">
                    <h1>{sport.sportName}</h1>
                    <p>{sport.description}</p>
                </div>
                <div className="form-section">
                    <div className="calendar-container">
                        <h3>Fecha</h3>
                        <Calendar value={selectedDate} onChange={(e) => setSelectedDate(e.value)} />
                    </div>
                    <div className="schedule-section">
                        <h3>Horario</h3>
                        <Schedule value={selectedSchedule} onChange={(hour) => setSelectedSchedule(hour)} />
                        </div>
                    {sportName === 'Piscina' && (
                        <div className="calle-section">
                            <h3>Calle</h3>
                            <form>
                                <select name="lane" id="lane" onChange={(e) => setSelectedLane(e.target.value)}>
                                    <option value="1">Calle 1</option>
                                    <option value="2">Calle 2</option>
                                </select>
                            </form>
                        </div>
                    )}
                </div>
                <button className="add-to-cart-button" onClick={() => {setIsModalOpen(true)}}>Reservar</button>

                {isModalOpen && (
                // TODO: Fix Footer background color
                <div className="modal-overlay">
                    <div className="modal">
                        <h4>¿Quiere confirmar la reserva?</h4>
                        {error && <p className="error-message">{error}</p>}
                        <div className="modal-buttons">
                            <button className="cancel-button" onClick={() => setIsModalOpen(false)}>
                                Cancelar
                            </button>

                            <button className="confirm-button blue" onClick={handleBook}>
                                Confirmar
                            </button>
                        </div>
                    </div>
                </div>  
                )}

            </div>
        </div>

    )
}

export default SportDetail;