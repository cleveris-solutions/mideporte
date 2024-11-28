import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../auth/AuthContext';
import './../assets/styles/screens/BookingsList.css';
import BookingCard from './../components/BookingCard';
import { Link } from 'react-router-dom';

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

    const sortedBookings = bookings.sort((a, b) => new Date(b.start) - new Date(a.start));

    return (
        <div className="bookings-list">
            <header className="bookings-header">
                <h1>Tu lista de reservas</h1>
                <h2>Estas son tus reservas confirmadas (en azul), canceladas (en rojo) y antiguas (en gris)</h2>
            </header>

            <div className="bookings-container">
                
            </div>

            <div className="bookings-container">
                {sortedBookings.length > 0 ? (
                    sortedBookings.map((booking) => (
                        <BookingCard 
                            key={booking.id} 
                            bookingId={booking.id}
                            installation={booking.installation.name} 
                            details={booking.details} 
                            date={booking.start} 
                            image={booking.installation.type.image} 
                            status={booking.status}
                        />
                    ))
                ) : (
                    <div className="no-bookings">
                        <p>Todavía no tienes ninguna reserva.</p>
                        <Link to="/deportes">Para crear una reserva, pulsa aquí</Link>
                    </div>
                    )}
            </div>


        </div>
    );
};

export default BookingsList;
