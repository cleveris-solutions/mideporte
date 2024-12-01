import { useContext, useEffect, useState } from "react";
import './../assets/styles/components/Schedule.css';
import { AuthContext } from "../auth/AuthContext";

const Schedule = ({ value, onChange , date, installationId}) => {
    const [availableHours, setAvailableHours] = useState([]);
    const [everyHour, SetEveryHour] = useState([]);
    
    // const everyHour = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"];
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
        
    }, [date, installationId,user.token]);
    
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