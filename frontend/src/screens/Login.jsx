import Cookies from 'js-cookie';
import { useContext, useState } from "react";
import Weather from '../components/layout/Weather';
import puebloImage from './../assets/images/pueblo.jpeg';
import './../assets/styles/screens/Login.css';
import { AuthContext } from './../auth/AuthContext';

const Login = () => {
    const [DNI, setDNI] = useState('');
    const [error, setError] = useState('');

    const { login } = useContext(AuthContext)
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        clearCookies();
    
        try {
            const response = await fetch(`/api/v1/users/authenticate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ DNI: DNI }),
            });

            const cookies = document.cookie.split(';');
            
            if (!response.ok) {
                const errorMessage = await response.json();
                throw new Error(errorMessage.error);
            }

            const data = await response.json();
            login(data); 
        } catch (err) {
            setError(err.message);
        }
    };

    const clearCookies = () => {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const eqPos = cookie.indexOf('=');
            const name = eqPos > -1 ? cookie.substring(0, eqPos).trim() : cookie.trim();
            Cookies.remove(name);
        });
    };


    return(
        <div className="login-container">
            <div className="login-info">
                <div className="login-header">
                    <h1>¡Bienvenido/a, cruceño/a!</h1>
                    <h2>¿Listo/a para reservar tu pista?</h2>
                    <div className="description-container">
                        <h3>
                            Este es el sistema de reservas  gratuito para todos los censados en 
                            Villanueva de las Cruces.
                        </h3>
                        <h3>
                            Para poder acceder deberemos comprobar si estás censado. 
                        </h3>
                    </div>
                </div>

                <div className="login-form">
                    <form onSubmit={handleSubmit}>
                        <h3>Introduzca su DNI:</h3>
                        <input
                            type="text"
                            value={DNI}
                            onChange={(e) => setDNI(e.target.value)}
                            placeholder="DNI:"
                        />
                        <button type="submit">Confirmar</button>
                    </form>
                </div>
                
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </div>

            <div className="pueblo-image-container">
                <img 
                    src={puebloImage}
                    alt="Pueblo de Villanueva de las Cruces" 
                    className="pueblo-image"
                />
            </div>

            <Weather />
        </div>
    )

}


export default Login;