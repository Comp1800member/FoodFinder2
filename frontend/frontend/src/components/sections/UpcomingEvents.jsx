import React, { useEffect, useState } from 'react';

const UpcomingEvents = () => {
    const [events1, setEvents1] = useState([]);  // Using `events1` to match your requirement

    useEffect(() => {
        // Fetch events from the FastAPI backend
        fetch("/upcoming-events")
            .then((response) => response.json())
            .then((data) => {
                // Map through the fetched events and transform them into the structure you need
                const transformedEvents = data.events.map((event) => {
                    return {
                        start_time: event.start_time,  // Use start_time as it is or format it if needed
                    };
                });
                // Set the transformed events list
                setEvents1(transformedEvents);
            })
            .catch((error) => {
                console.error("Error fetching events:", error);
            });
    }, []);

    return (
        <div>
            <h1>Upcoming Events</h1>
            {events1.length > 0 ? (
                <ul>
                    {events1.map((event, index) => (
                        <li key={index}>
                            <p>Start Time: {event.start_time}</p> {/* Display start_time */}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No upcoming events found.</p>
            )}
        </div>
    );
};

export default UpcomingEvents;