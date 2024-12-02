import { useContext, useEffect, useState } from "react";
import './../assets/styles/components/Schedule.css';
import { AuthContext } from "../auth/AuthContext";

const Schedule = ({ value, onChange , date, installationId}) => {
    const [availableHours, setAvailableHours] = useState([]);
    const [everyHour, SetEveryHour] = useState([]);
    
    const { user } = useContext(AuthContext);

    useEffect(() => {

        const fetchAvailableHours = async () => {
            try {
                const response = await fetch(`/api/v1/installations/availableSchedule/${installationId}/${date}`, {
                    headers: {
                        'Authorization': `Token ${user.token}`
                    }
                });
                const data = await response.json();
                setAvailableHours(data);
            } catch (error) {
                console.error("Error fetching data: ", error);
            }
        };


        const fetchEveryHours = async () => {
            try {
                const response = await fetch(`/api/v1/installations/schedule/${installationId}/${date}`, {
                    headers: {
                        'Authorization': `Token ${user.token}`
                    }
                });
                const data = await response.json();
                SetEveryHour(data);
            } catch (error) {
                console.error("Error fetching data: ", error);
            }
        };
    
        fetchAvailableHours();
        fetchEveryHours();
        
    }, [date, installationId]);
    
    const handleHourClick = (hour) => {
        if (hour !== value) {
            onChange(hour);
        } else {
            onChange(null); 
        }
    };

    return (
        <div className="schedule-container">
            {everyHour.map((hour) => (
                <button
                    key={hour}
                    onClick={() => handleHourClick(hour)}
                    disabled={!availableHours.includes(hour)}
                    className={`hour-button 
                        ${availableHours.includes(hour) ? 'available' : 'unavailable'} 
                        ${value === hour ? 'selected' : ''}`}>
                    {hour}
                </button>
            ))}
        </div>
    );
};

export default Schedule;