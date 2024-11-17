import React, { useEffect, useState } from 'react';
// import { AuthContext } from './../auth/AuthContext';
import './../assets/styles/screens/BookingsList.css';
import { sportImages } from './../utils/imageMapping';
import BookingCard from './../components/BookingCard';
import { Link } from 'react-router-dom';

const BookingsList = () => {
  //const { user } = useContext(AuthContext);
  const [bookings, setBookings] = useState([]);
    
    useEffect(() => {
		// TODO: Fetch data from API
        const booking1 = { sportName: 'Fútbol', details: 'Pista para 14 personas', date: 'Lunes, 25 de agosto, 11:00-12:00' };
        const booking2 = { sportName: 'Pádel', details: 'Pista para 4 personas', date: 'Miércoles, 27 de agosto, 16:00-17:00' };
        const booking3 = { sportName: 'Pádel', details: 'Pista para 4 personas', date: 'Miércoles, 27 de agosto, 17:00-18:00' };
        const booking4 = { sportName: 'Baloncesto', details: 'Pista para 10 personas', date: 'Jueves, 28 de agosto, 20:00-21:00' };
        
        setBookings([booking1, booking2, booking3, booking4]);
    }, []);

    return (
        <div className="bookings-list">
            <header className="bookings-header">
                <h1>Lista de reservas</h1>
                <h3>Estas son tus reservas confirmadas.</h3>
            </header>

            <div className="bookings-container">
                {bookings.map((booking, index) => (
                    // TODO: Change link to booking details by id
                    // TODO: Check if user is logged in
					<Link to={`/reservas/${booking.sportName}`} style={{textDecoration:'none'}}>
						<BookingCard 
							key={index} 
							sport={booking.sportName} 
							details={booking.details} 
							date={booking.date} 
							image={sportImages[booking.sportName]} 
							hoverEffect={true}
						/>
					</Link>
				))}
            </div>
        </div>
    );
};

export default BookingsList;
