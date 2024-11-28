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
                const errorMessage = await response.json();
                throw new Error(errorMessage.error);
            }

            
            window.location.reload();
        } catch (err) {
			// Error handling might be improved
            setError(err.message);
			console.error(error)
        }
    };
	
    function buildDate(isoDate) {
        const date = new Date(isoDate);
    
        const day = date.getUTCDate().toString().padStart(2, '0');
        const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
        const year = date.getUTCFullYear();
        const hours = date.getUTCHours().toString().padStart(2, '0');
        const minutes = date.getUTCMinutes().toString().padStart(2, '0');
    
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }
    
    return (
		<div className='booking-card-container'> 
			<div className={`booking-card ${date && new Date(date).toISOString() < new Date(Date.now() + 60 * 60 * 1000).toISOString()
                ? 'gray'
                : status === 'Cancelada' ? 'gradient-red' : 'gradient-blue'}`}>

				<img className="booking-image" src={image} alt={installation} />
				
				<div className="booking-details">
					<h3 className="booking-title">{installation}</h3>
					<p className="booking-description">{details}</p>
					<span className="booking-date">{buildDate(date)}</span>
                    <span>{status}</span>
				</div>
				{status !== 'Cancelada' && 
                date && new Date(date).toISOString() > new Date(Date.now() + 120 * 60 * 1000).toISOString() && 
                    <div className='booking-cancel' onClick={() => {setIsModalOpen(true); setError(null)}}>
                        &#10005;
                    </div>
                }


                

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
