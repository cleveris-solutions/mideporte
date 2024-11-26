import { useContext, useState } from 'react';
import './../assets/styles/components/BookingCard.css';
import './../assets/styles/modal.css';
import { AuthContext } from '../auth/AuthContext';

const BookingCard = ({bookingId, installation, details, date, image, status }) => {

    const [isModalOpen, setIsModalOpen] = useState(false);
	const [error, setError] = useState('');

    const { user } = useContext(AuthContext);
	
	const handleCancel = async (e) => {
        e.preventDefault();
    
        try {
            const response = await fetch(`/api/v1/bookings/cancel/${bookingId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${user.token}`,
                },
            });

            if (!response.ok) {
                throw new Error('Ha ocurrido un error');
            }

            const data = await response.json();
            window.location.reload();
        } catch (err) {
			// Error handling might be improved
            setError(err.message);
			console.error(error)
        }
    };
	
    const buildDate = (date) => {
        const dateObj = new Date(date);
        return `${dateObj.getDate()}/${dateObj.getMonth() + 1}/${dateObj.getFullYear()} ${dateObj.getHours()}:${dateObj.getMinutes() < 10 ? '0' + dateObj.getMinutes() : dateObj.getMinutes()}`;
    }

    return (
		<div className='booking-card-container'> 
			<div className={`booking-card ${status === 'Cancelada' ? 'gradient-red' : 'gradient-blue'}`}>

				<img className="booking-image" src={image} alt={installation} />
				
				<div className="booking-details">
					<h3 className="booking-title">{installation}</h3>
					<p className="booking-description">{details}</p>
					<span className="booking-date">{buildDate(date)}</span>
                    <span>{status}</span>
				</div>
				
				{status !== 'Cancelada' && <div className='booking-cancel' onClick={() => {setIsModalOpen(true)}}>
					&#10005;
				</div>}

                

                {isModalOpen && (
                <div className="modal-overlay">
                    <div className="modal">
                        <h4>¿Seguro que deseas cancelar esta reserva?</h4>
                        {error && <p className="error-message">{error}</p>}
                        <div className="modal-buttons">
                            <button className="cancel-button" onClick={() => setIsModalOpen(false)}>
                                No, mantener reserva
                            </button>

                            <button className="confirm-button red" onClick={handleCancel}>
                                Sí, cancelar
                            </button>
                        </div>
                    </div>
                </div>
            )}

			</div>
		</div>
    );
};

export default BookingCard;
