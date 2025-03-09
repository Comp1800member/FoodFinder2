import { useEffect, useState } from "react";    
//import { collection, getDocs } from 'firebase/firestore'
//import {db} from '../firebase/config'
import EventScroller from "../EventScroller";
import { RevealScrolling } from "../RevealScrolling";
import UpcomingEvents from "./UpcomingEvents.jsx";

export const About = () => {
    const [events1, setEvents1] = useState([]);  // State to store events fetched from backend

    // Function to fetch upcoming events from the backend
    async function getUpcomingEvents() {
      try {
        const response = await fetch("http://localhost:8000/upcoming-events");
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();  // Parse JSON response
        console.log(data.events);  // This will contain the list of events

        // Transform events to match your desired structure
        const transformedEvents = data.events.map((event) => {
            const startTime = new Date(event.start_time);
            const endTime = new Date(event.end_time);

            const startDate = startTime.toISOString().split('T')[0];
            const start_time = startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const end_time = endTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });  // Extract time (HH:MM)
            return {
                name: event.name,
                startDate,
                start_time,  // Add more fields as needed
                end_time,
                location: event.location
            };
        });

        setEvents1(transformedEvents);  // Set the events1 state with the transformed data

      } catch (error) {
        console.error("Error fetching events:", error);
      }
    }

    // Call the function to fetch upcoming events
    useEffect(() => {
      getUpcomingEvents();  // Fetch events when component mounts
    }, []);

        // let events = [
        //     {
        //         id: 1,
        //         title: "Mountain Madness",
        //         date: "Date: March 8, 2025",
        //         time: "Time: 8:30 AM",
        //         location: "Location: CSSS",
        //         image: "https://sfucsss.org/STATIC_URL/csss_static/logo.png",
        //     },
        //     {
        //         id: 2,
        //         title: "SFU Surge Picnic",
        //         date: "Date: March 15, 2025",
        //         time: "Time: 5:00 PM",
        //         location: "Location: Student Union Building",
        //         image: "https://go.sfss.ca/clubs/831/logo",
        //     },
        //     {
        //         id: 3,
        //         title: "SFU Shockwave BBQ",
        //         date: "Date: April 11, 2025",
        //         time: "Time: 12:00 PM",
        //         location: "Location: SFU TASC1 9204",
        //         image: "https://go.sfss.ca/clubs/676/logo",
        //     },
        //     {
        //         id: 4,
        //         title: "SFU Anime Ice Breaker",
        //         date: "Date: April 16, 2025",
        //         time: "Time: 2:00 PM",
        //         location: "Location: SFU Blusson Hall",
        //         image: "https://go.sfss.ca/clubs/356/logo",
        //     },
        //     {
        //         id: 5,
        //         title: "SFU Enactus Outing",
        //         date: "Date: April 16, 2025",
        //         time: "Time: 3:30 PM",
        //         location: "Location: Student Union Building",
        //         image: "https://go.sfss.ca/clubs/98/logo",
        //     },
        // ]

        const SplitComponent = () => {
            return (
                
              <div className="w-full max-w-md border rounded-lg overflow-hidden shadow-md">
                {/* Top part with image */}
                <div className="w-full h-48">
                  <img 
                    src="https://reactjs.org/logo-og.png" 
                    alt="Description" 
                    className="w-full h-full object-cover"
                  />
                </div>
                
                {/* Bottom part with text */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
                <div className="rounded-xl p-6">
                  <h3 className="text-xl text-black font-bold mb-2">Free Food</h3>
                  <p className="text-gray-700">
                    This is where you can place your description text. You can add as much content
                    as needed and style it however you'd like.
                  </p>
                </div>
              </div>
            );
          };
    return <section 
    id="about" 
    className="min-h-screen flex items-center py-20 "
    >
        <RevealScrolling>
        <div className="w-full grid justify-center ml-9 px-2">
        <h2 id="Upcoming-events" className="text-6xl font-Lemon flex justify-center font-bold mb-8 bg-gradient-to-r from-green-700 to-green-600 bg-clip-text text-transparent">
                Upcoming Events
        </h2>
            {/*
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="rounded-xl p-6 hover:-translate-y-1 transition-all">
                    <h3 className="text-xl text-black font-bold mb-4">
                        First Foods
                    </h3>
                    <div className="flex flex-wrap gap-2">
                        {foodOne.map((tech, key) => (
                            <span 
                            key = {key}
                            className="bg-blue-500/10 text-blue-500 py-1 px-3 rounded-full text-sm hover:bg-blue-500/20
                                            hover:shadow-[0_2px_8px_rgba(59, 130, 2246, 0.2)] transition">
                                                {tech}
                            </span>
                        ))}
                    </div>
                </div>
                
                <div className="p-6 rounded-xl border-white/10 border hover:-translate-y-1 transition-all">
                        <h3 className="text-xl text-black font-bold mb-4">
                            Foods
                        </h3>
                        <ul className="list-disc list-inside text-gray-300 space-y-2">
                            <li>
                                    Food1 
                            </li>
                            <li>
                                Food2
                            </li>
                        </ul>
                </div>
            </div>
            <div className="mt-8">
                <SplitComponent />
            </div>
            */}
            <div className="w-full mt-2 rounded-lg overflow-hidden p-2">
                <EventScroller events1={events1} />
            </div>
            
        </div>
        </RevealScrolling>
        
    </section>
};