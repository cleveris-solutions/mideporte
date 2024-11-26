import { useContext, useState } from "react";
import './../assets/styles/screens/Login.css';
import puebloImage from './../assets/images/pueblo.jpeg';
import Weather from '../components/layout/Weather';
import Contacto from '../components/layout/Contacto';
import { AuthContext } from './../auth/AuthContext';

const Login = () => {
    const [DNI, setDNI] = useState('');
    const [error, setError] = useState('');

    const { login } = useContext(AuthContext)
    
    const handleSubmit = async (e) => {
        e.preventDefault();
    
        try {
            // TODO: Add the URL of the backend
            const response = await fetch(`/api/v1/users/authenticate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ DNI: DNI }),
            });

            if (!response.ok) {
                throw new Error('Invalid code');
            }

            const data = await response.json();
            login(data); 
        } catch (err) {
            setError(err.message);
        }
    };

    const handleSubmitTemporary = (e) => {
        e.preventDefault();

        setTimeout(() => {
            const simulatedResponse = { user: { name: 'Javier Santos', dni: DNI } };
            login(simulatedResponse); 
        }, 500); 
    };
    

    return(
        <div className="login-container">
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

            <div className="pueblo-image-container">
                <img 
                    src={puebloImage}
                    alt="Pueblo de Villanueva de las Cruces" 
                    className="pueblo-image"
                />
            </div>

            <Weather />
            <Contacto />
        </div>
    )

}


export default Login;