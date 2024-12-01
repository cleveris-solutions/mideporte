import { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from './../auth/AuthContext';
import SportCard from './../components/SportCard';
import Weather from '../components/layout/Weather';
import './../assets/styles/screens/Home.css';

const Home = () => {

    const [sports, setSports] = useState([]);

	const { user } = useContext(AuthContext); 
    
    useEffect(() => {
        
        const fetchSports = async () => {
            fetch('/api/v1/installations/sports', {
				headers: {
					'Authorization': `Token ${user.token}`
				}
			})
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    setSports(data);
                })
                .catch((error) => {
                    console.error("Error fetching data: ", error);
                })
        };

        fetchSports();
    }, [user.token]);
    
	return (
		<div className='home-container'>
			<div className='home-header'>
				<h1>{user.user.name}, aquí puedes reservar pista</h1>
				<h2>Estas son las instalaciones disponibles, selecciona la que te interese.</h2>
			</div>

			<div className='cards-container'>
				{sports.map((sport, index) => (
					<Link to={`/deportes/${sport.name}`} class={"sport-link"} style={{textDecoration:'none'}} key={index}>
						<SportCard 
							sport={sport.name} 
							description={sport.description} 
							image={`/static${sport.image}`}
							hoverEffect={true}
						/>
					</Link>
				))}
			</div>

			<Weather />
		</div>
	);

}


export default Home;