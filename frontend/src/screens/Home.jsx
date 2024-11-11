import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import SportCard from './../components/SportCard';

import baloncesto_image from './../assets/images/baloncesto.png';
import futbol_image from './../assets/images/futbol.png';
import padel_image from './../assets/images/padel.png';
import piscina_image from './../assets/images/piscina.png';
import './../assets/styles/screens/Home.css';


const Home = () => {

    const [sports, setSports] = useState([]);
    
	const images ={
		'Padel': padel_image, 
		'Fútbol': futbol_image, 
		'Baloncesto': baloncesto_image, 
		'Piscina': piscina_image
	}

    useEffect(() => {
		// TODO: Fetch data from API :D
        const sport1 = { sportName: 'Padel', description: 'Pista para 4 personas', message: null };
        const sport2 = { sportName: 'Fútbol', description: 'Pista para 14 personas', message: 'Tienes una pista reservada.' };
        const sport3 = { sportName: 'Baloncesto', description: 'Pista para 10 personas', message: null };
        const sport4 = { sportName: 'Piscina', description: '2 calles individuales', message: null };
        
        setSports([sport1, sport2, sport3, sport4]);
    }, []);
    
	return (
		<div className='home-container'>
			<div className='home-header'>
				<h1>Reserva ya tu pista</h1>
				<h2>Reservas gratuitas para todos los censados en Villanueva de las Cruces</h2>
			</div>

			<div className='cards-container'>
				{sports.map((sport, index) => (
					<Link to={`/deportes/${sport.sportName}`} style={{textDecoration:'none'}}>
						<SportCard 
							key={index} 
							sport={sport.sportName} 
							description={sport.description} 
							message={sport.message} 
							image={images[sport.sportName]} 
							hoverEffect={true}
						/>
					</Link>
				))}
			</div>
		</div>
	);

}


export default Home;