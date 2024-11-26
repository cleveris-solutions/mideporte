import { useContext, useState } from "react";
import './../assets/styles/screens/Login.css';
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
                throw new Error('Este DNI no pertenece a nadie censado en Villanueva de las Cruces.');
            }

            const data = await response.json();
            login(data); 
        } catch (err) {
            setError(err.message);
        }
    };

    return(
        <div className="login-container">
            <div className="login-header">
                <h1>Bienvenido</h1>
                <h3>
                    Este es el sistema de reservas  gratuito para todos los censados en 
                    Villanueva de las Cruces
                </h3>
                <h3>
                    Para poder acceder deberemos comprobar si estás censado. 
                </h3>
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
    )

}


export default Login;