import { useContext, useState } from "react";
import './../assets/styles/screens/Login.css';
import { AuthContext } from './../auth/AuthContext';

const Login = () => {
    const [code, setCode] = useState('');
    const [error, setError] = useState('');

    const { login } = useContext(AuthContext)
    const backendURL = process.env.REACT_APP_BACKEND_URL;
    
    const handleSubmit = async (e) => {
        e.preventDefault();
    
    try {
        // TODO: Add the URL of the backend
        const response = await fetch(`${backendURL}/api/v1/user/validate-login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
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
            const simulatedResponse = { user: { name: 'Javier Santos', dni: code } };
            login(simulatedResponse); 
        }, 500); 
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
                <form onSubmit={handleSubmitTemporary}>
                    <h3>Introduzca su DNI:</h3>
                    <input
                        type="text"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
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