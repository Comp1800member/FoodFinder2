// components/EventCard.jsx
const EventCard = ({ event }) => {
    return (
      <div className="flex-none w-64 bg-white rounded-lg overflow-hidden shadow-sm">
        <div className="h-48 relative">
          <img 
            src={event.image} 
            alt={event.title}
            className="w-full h-full object-cover" 
          />
          <span className="absolute top-3 left-3 bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded">
            {event.tag}
          </span>
        </div>
        <div className="p-4">
          <h3 className="font-bold text-gray-900">{event.title}</h3>
          <div className="mt-2 space-y-1">
            {/* Event details with icons */}
          </div>
        </div>
      </div>
    );
  };
  
  export default EventCard;