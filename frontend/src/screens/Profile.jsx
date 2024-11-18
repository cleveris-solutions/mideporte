import { useContext, useState } from 'react';
import { AuthContext } from '../auth/AuthContext';
import './../assets/styles/screens/Profile.css';
import './../assets/styles/modal.css';

const Profile = () => {

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [error, setError] = useState('');
    
    const { logout } = useContext(AuthContext);
    const { user } = useContext(AuthContext);

    const handleLogOut = () => {
        logout();   
    }

    return(
        <div className="profile">
            <header className="profile-header">
                <h1>Perfil de {user.user.name}</h1>
                <button onClick={() => {setIsModalOpen(true)}}>Cerrar sesión</button>
            </header>

            <ul className="profile-info">
                <li>
                    Nombre: 
                    <span>{user.user.name}</span>
                </li>
                <li>
                    DNI:
                    <span>{user.user.dni}</span>
                </li>
            </ul>

            {isModalOpen && (
                // TODO: Fix Footer background color
                <div className="modal-overlay">
                    <div className="modal">
                        <h4>¿Quiere cerrar sesión?</h4>
                        {error && <p className="error-message">{error}</p>}
                        <div className="modal-buttons">
                            <button className="cancel-button" onClick={() => setIsModalOpen(false)}>
                                Cancelar
                            </button>

                            <button className="confirm-button red" onClick={handleLogOut}>
                                Sí, cerrar sesión
                            </button>
                        </div>
                    </div>
                </div>
            )}

        </div>    )
}


export default Profile;