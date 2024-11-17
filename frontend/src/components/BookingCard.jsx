import './../assets/styles/components/BookingCard.css';

const BookingCard = ({ sport, details, date, image, hoverEffect }) => {
    return (
		<div className='booking-card-container'> 
			<div className={`booking-card ${hoverEffect ? 'hover-effect' : ''}`}> 
				<img className="booking-image" src={image} alt={sport} />
				<div className="booking-details">
					<h3 className="booking-title">{sport}</h3>
					<p className="booking-description">{details}</p>
					<span className="booking-date">{date}</span>
				</div>
			</div>
		</div>
    );
};

export default BookingCard;
