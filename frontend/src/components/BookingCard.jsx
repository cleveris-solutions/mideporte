import { useState } from 'react';
import './../assets/styles/components/BookingCard.css';
import './../assets/styles/modal.css';

const BookingCard = ({bookingId, sport, details, date, image }) => {

    const [isModalOpen, setIsModalOpen] = useState(false);
	const [error, setError] = useState('');
	
	const handleCancel = async (e) => {
        e.preventDefault();
    
        try {
            const response = await fetch(`/api/v1/booking/cancel/${bookingId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Invalid code');
            }

            const data = await response.json();
        } catch (err) {
			// Error handling might be improved
            setError(err.message);
			console.error(error)
        }
    };
	
    return (
		<div className='booking-card-container'> 
			<div className={'booking-card'}> 

				<img className="booking-image" src={image} alt={sport} />
				
				<div className="booking-details">
					<h3 className="booking-title">{sport}</h3>
					<p className="booking-description">{details}</p>
					<span className="booking-date">{date}</span>
				</div>
				
				<div className='booking-cancel' onClick={() => {setIsModalOpen(true)}}>
					&#10005;
				</div>

                

                {isModalOpen && (
                // TODO: Fix Footer background color
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
