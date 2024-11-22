import { Calendar } from 'primereact/calendar';
import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Schedule from '../components/Schedule';
import SportCard from '../components/SportCard';
import { sportImages } from './../utils/imageMapping';
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
    const [error, setError] = useState('');
    
    const { sportName } = useParams();
    const { user } = useContext(AuthContext);
    
    useEffect(() => {
        const fetchSport = async () => {
            try {
                const response = await fetch(`/api/v1/installations/type/${sportName}`);
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
        console.log(user)
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
                    start_time: selectedDate.toISOString().split("T")[0] + " " + selectedSchedule
                })
            });

            if (!response.ok) {
                throw new Error('Something went wrong');
            } else {
                setError("")
                setIsModalOpen(false)
                window.location.reload();
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
    
    return (
        <div className="sport-detail-container">
            <div className="card-section">
                <SportCard 
                    sport={sportName} 
                    description={installations.length > 0 ? installations[0].type.description : ''} 
                    image={installations.length > 0 ? installations[0].type.image : ''} 
                />
            </div>
            <div className="info-section">
                <div className="sport-header">
                    <h1>{installations.length > 0 ? installations[installation].name : ''}</h1>
                    <p>{installations.length > 0 ? installations[installation].description : ''}</p>
                </div>
                <div className="form-section">
                    <div className="calendar-container">
                        <h3>Fecha</h3>
                        
                        <Calendar value={selectedDate} onChange={(e) => setSelectedDate(e.value)} />
                    </div>
                    <div className="schedule-section">
                        <h3>Horario</h3>
                        <Schedule 
                            value={selectedSchedule} 
                            onChange={(hour) => setSelectedSchedule(hour)} 
                            date={selectedDate.toISOString().split("T")[0]}
                            installationId={installations.length > 0 ? installations[installation].id : 1}/>
                    </div>
                    {installations.length > 1 && (
                        <div>
                            <h3>{displayInstallation()}</h3>
                            <form>
                                <select name="installation" id="installation" onChange={(e) => setInstallation(e.target.value)}>
                                    {installations.map((inst, index) => (
                                        <option key={index} value={index}>{displayInstallation()}: {index + 1}</option>
                                    ))}
                                </select>
                            </form>
                        </div>
                    )}
                </div>
                <button className="add-to-cart-button" onClick={() => {setIsModalOpen(true)}}>Reservar</button>

                {isModalOpen && (
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