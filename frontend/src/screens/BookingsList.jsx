import React, { useContext, useEffect, useState } from 'react';
import './../assets/styles/screens/BookingsList.css';
import BookingCard from './../components/BookingCard';
import Weather from '../components/layout/Weather';
import Contacto from '../components/layout/Contacto';
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

    const sortedBookings = bookings.sort((a, b) => new Date(b.start) - new Date(a.start));

    return (
        <div className="bookings-list">
            <header className="bookings-header">
                <h1>Tu lista de reservas</h1>
                <h2>Estas son tus reservas confirmadas (en azul) y canceladas (en rojo).</h2>
            </header>

            <div className="bookings-container">
                {sortedBookings.map((booking) => (
                    <BookingCard 
                        key={booking.id} 
                        bookingId={booking.id}
                        installation={booking.installation.name} 
                        details={booking.details} 
                        date={booking.start} 
                        image={booking.installation.type.image} 
                        status={booking.status}
                    />
				))}
            </div>
            <div className='bottom'>
                <Weather />
                <Contacto />
            </div>
        </div>
    );
};

export default BookingsList;
