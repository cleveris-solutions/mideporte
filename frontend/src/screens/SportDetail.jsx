import { addLocale, locale } from 'primereact/api';
import { Calendar } from 'primereact/calendar';
import { useContext, useEffect, useState} from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Weather from '../components/layout/Weather';
import Schedule from '../components/Schedule';
import SportCard from '../components/SportCard';
import { AuthContext } from './../auth/AuthContext';

import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.min.css';
import 'primereact/resources/themes/saga-blue/theme.css';
import './../assets/styles/screens/SportDetail.css';

const SportDetail = () => {
    const [installations, setInstallations] = useState([]);
    const [installation, setInstallation] = useState(null);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [selectedSchedule, setSelectedSchedule] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [reservationSuccess, setReservationSuccess] = useState(false);
    const [scheduleUpdateKey, setScheduleUpdateKey] = useState(0);
    const [error, setError] = useState('');

    const navigate = useNavigate();
    const { sportName } = useParams();
    const { user } = useContext(AuthContext);
    
    addLocale('es', {
        firstDayOfWeek: 1,
        dayNames: ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'],
        dayNamesShort: ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'],
        dayNamesMin: ['D', 'L', 'M', 'X', 'J', 'V', 'S'],
        monthNames: [
            'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
        ],
        monthNamesShort: [
            'ene', 'feb', 'mar', 'abr', 'may', 'jun', 
            'jul', 'ago', 'sep', 'oct', 'nov', 'dic'
        ],
        today: 'Hoy',
        clear: 'Limpiar',
    });
    
    locale('es');
    
    
    useEffect(() => {
        const fetchSport = async () => {
            try {
                const response = await fetch(`/api/v1/installations/type/${sportName}`, {
                    headers: {
                        'Authorization': `Token ${user.token}`
                    }
                });
                const data = await response.json();
                setInstallations(data);
    
                if (data.length > 0) {
                    setInstallation(0);
                }
            } catch (error) {
                console.error("Error fetching data: ", error);
            }
        };
    
        fetchSport();
    }, [sportName]);

	const handleBook = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/api/v1/bookings/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${user.token}`,
                },
                body: JSON.stringify({
                    user_id: user.user.DNI,
                    installation_id: installations[installation].id,
                    start_time: buildStartDate(selectedDate, selectedSchedule)
                })
            });

            if (!response.ok) {
                const errorMessage = await response.json();
                throw new Error(errorMessage.error);
            } else {
                setError("")
                setIsModalOpen(false)
                setReservationSuccess(true);

                // To update the schedule component when a reservation is made (and not the entire page)
                setScheduleUpdateKey((prevKey) => prevKey + 1);
    
                setTimeout(() => {
                    setReservationSuccess(false);
                }, 5000);
                
                //window.location.reload()
            }

            const data = await response.json();
        } catch (err) {
			// Error handling might be improved
            setError(err.message);
			console.error(error)
        }
    };

    const displayInstallation = () => {
        if (sportName === "Piscina") {
            return "Calle";
        } else {
            return "Instalación";
        }
    }

    const buildStartDate = (date, schedule) => {
        return date.toLocaleDateString("en-CA") + "T" + schedule + ":00Z";
    }

    return (
        <div className="sport-screen">
            <div className='sport-top-container'>
                <button className="back-button" onClick={() => navigate(-1)}>
                    ← Volver
                </button>
                <div className="sport-title">
                    <h1>{installations.length > 0 ? installations[installation].name : ''}</h1>
                </div>
                <button className="add-to-cart-button" onClick={() => {setIsModalOpen(true); setError(null)}}>
                    Reservar
                </button>
            </div>

            <div className='sport-bottom-container'>
                <div className="card-section">
                    <SportCard 
                        sport={sportName} 
                        description={installations.length > 0 ? installations[0].type.description : ''} 
                        image={installations.length > 0 ? installations[0].type.image : ''} 
                    />
                </div>

                <div className="center-section">
                    {installations.length > 1 && (
                        <div className="calle-container">
                            <h3>Calle:</h3>
                            <form>
                                <select 
                                    name="installation" 
                                    id="installation" 
                                    className="installation-select" 
                                    onChange={(e) => setInstallation(e.target.value)}
                                >
                                    {installations.map((inst, index) => (
                                        <option key={index} value={index}>
                                            {displayInstallation()}: {index + 1}
                                        </option>
                                    ))}
                                </select>
                            </form>
                        </div>
                    )}
                    
                    <div className="calendar-container">
                        <h3>Fecha:</h3>
                        <Calendar value={selectedDate} dateFormat="dd-mm-yy" 
                            onChange={(e) => setSelectedDate(e.value)} minDate={new Date(Date.now())} showIcon inline/>
                    </div>
                </div>

                <div className="schedule-section">
                    <h3>Horario:</h3>
                    <Schedule 
                        key={scheduleUpdateKey}
                        value={selectedSchedule} 
                        onChange={(hour) => setSelectedSchedule(hour)} 
                        date={selectedDate.toLocaleDateString("en-CA")}
                        installationId={installations.length > 0 ? installations[installation].id : 1}/>
                
                </div>
            </div>

            {isModalOpen && (
                <div className="modal-overlay">
                    <div className="modal">
                        <h4>¿Quiere confirmar la reserva?</h4>
                        {error && <p className="error-message">{error}</p>}
                        <div className="modal-buttons">
                            <button className="cancel-button" onClick={() => setIsModalOpen(false)}>
                                Cancelar
                            </button>

                            {!error &&
                            <button className="confirm-button green" onClick={handleBook}>
                                Confirmar
                            </button>}
                        </div>
                    </div>
                </div>  
                )}

            {reservationSuccess && (
                <div className="modal-overlay">
                    <div className="modal success-modal">
                        <h4>¡Reserva exitosa!</h4>
                        <p>Tu reserva se ha realizado con éxito.</p>
                        <button
                            className="confirm-button green"
                            onClick={() => setReservationSuccess(false)}
                        >
                            Vale, gracias
                        </button>
                    </div>
                </div>
            )}

            <div className='bottom'>
                <Weather />
            </div>

        </div>

    )
}

export default SportDetail;