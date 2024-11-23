import React, { useContext, useEffect, useState } from 'react';
import './../assets/styles/screens/BookingsList.css';
import BookingCard from './../components/BookingCard';
import { sportImages } from './../utils/imageMapping';
import { AuthContext } from '../auth/AuthContext';

const BookingsList = () => {
  const [bookings, setBookings] = useState([]);

  const { user } = useContext(AuthContext);
    
    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await fetch(`/api/v1/bookings/${user.user.DNI}`, {
                    headers: {
                        'Authorization': `Token ${user.token}`
                    }
                })
                const data = await response.json();
                setBookings(data.bookings);
            } catch (error) {
                console.error("Error fetching data: ", error);
            }
        };
        
        fetchBookings();
        
    }, [user]);

    console.log(bookings)
    
    return (
        <div className="bookings-list">
            <header className="bookings-header">
                <h1>No se asusten, funciona todo ok, estamos esperando a un cambio en los serializers para que lo vean lindo :D</h1>
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
                        date={booking.start} 
                        image={sportImages[booking.sportName]} 
                    />
				))}
            </div>
        </div>
    );
};

export default BookingsList;
