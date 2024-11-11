import { useEffect, useState } from "react";
import './../assets/styles/components/Schedule.css';

const Schedule = ({ value, onChange }) => {
    const [availableHours, setAvailableHours] = useState([]);
    const everyHour = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];

    useEffect(() => {
        // Fetch the data from the API. :D
        // At the moment, it's hardcoded
        setAvailableHours([9, 10, 11, 12, 15, 16, 19, 20]);
    }, []);

    const handleHourClick = (hour) => {
        if (hour !== value) {
            onChange(hour);
        } else {
            onChange(null); 
        }
    };

    const formatHourRange = (hour) => `${hour}:00 - ${hour + 1}:00`;

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
                    {formatHourRange(hour)}
                </button>
            ))}
        </div>
    );
};

export default Schedule;