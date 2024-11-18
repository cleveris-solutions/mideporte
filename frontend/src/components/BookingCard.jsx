import { useState } from 'react';
import './../assets/styles/components/BookingCard.css';

const BookingCard = ({bookingId, sport, details, date, image }) => {

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
			console.log(error)
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
				
				<div className='booking-cancel' onClick={handleCancel}>
					&#10005;
				</div>

			</div>
		</div>
    );
};

export default BookingCard;
