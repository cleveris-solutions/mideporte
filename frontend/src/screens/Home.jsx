import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { sportImages } from './../utils/imageMapping';
import SportCard from './../components/SportCard';
import './../assets/styles/screens/Home.css';

const Home = () => {

    const [sports, setSports] = useState([]);
    
    useEffect(() => {
        
        const fetchSports = async () => {
            fetch('/api/v1/installations/sports')
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
    }, [sports]);
    
	return (
		<div className='home-container'>
			<div className='home-header'>
				<h1>Reserva ya tu pista</h1>
				<h2>Reservas gratuitas para todos los censados en Villanueva de las Cruces</h2>
			</div>

			<div className='cards-container'>
				{sports.map((sport, index) => (
					<Link to={`/deportes/${sport.name}`} style={{textDecoration:'none'}} key={index}>
						<SportCard 
							sport={sport.name} 
							description={sport.description} 
							image={sport.image} 
							hoverEffect={true}
						/>
					</Link>
				))}
			</div>
		</div>
	);

}


export default Home;