import React, { useEffect, useState } from 'react';
import './../assets/styles/screens/BookingsList.css';
import BookingCard from './../components/BookingCard';
import { sportImages } from './../utils/imageMapping';

const BookingsList = () => {
  const [bookings, setBookings] = useState([]);
    
    useEffect(() => {
		// TODO: Fetch data from API
        const booking1 = { id: 1, sportName: 'Fútbol', details: 'Pista para 14 personas', date: 'Lunes, 25 de agosto, 11:00-12:00' };
        const booking2 = { id: 2, sportName: 'Pádel', details: 'Pista para 4 personas', date: 'Miércoles, 27 de agosto, 16:00-17:00' };
        const booking3 = { id: 3, sportName: 'Pádel', details: 'Pista para 4 personas', date: 'Miércoles, 27 de agosto, 17:00-18:00' };
        const booking4 = { id: 4, sportName: 'Baloncesto', details: 'Pista para 10 personas', date: 'Jueves, 28 de agosto, 20:00-21:00' };
        
        setBookings([booking1, booking2, booking3, booking4]);
    }, []);

    return (
        <div className="bookings-list">
            <header className="bookings-header">
                <h1>Lista de reservas</h1>
                <h2>Estas son tus reservas confirmadas.</h2>
            </header>

            <div className="bookings-container">
                {bookings.map((booking) => (
                    <BookingCard 
                        key={booking.id} 
                        bookingId={booking.id}
                        sport={booking.sportName} 
                        details={booking.details} 
                        date={booking.date} 
                        image={sportImages[booking.sportName]} 
                    />
				))}
            </div>
        </div>
    );
};

export default BookingsList;
