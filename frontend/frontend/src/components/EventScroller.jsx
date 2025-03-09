// components/EventScroller.jsx
import { useRef } from 'react';
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";


const EventScroller = ({ events1, events, title = "Event1" }) => {
  const NextArrow = (props) => {
    const { className, style, onClick } = props;
    return (
      <div
        className={className}
        style={{ 
          ...style, 
          display: "block", 
          background: "rgba()",
          borderRadius: "50%"
        }}
        onClick={onClick}
      />
    );
  };
  const PrevArrow = (props) => {
    const { className, style, onClick } = props;
    return (
      <div
        className={className}
        style={{ 
          ...style, 
          display: "block", 
          background: "rgba()",
          borderRadius: "50%"
        }}
        onClick={onClick}
      />
    );
  };
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
    nextArrow: <NextArrow/>,
    prevArrow: <PrevArrow/>
  };

  return (
    <div className="w-3/4 m-auto">
            <style jsx>{`
        .slick-prev:before,
        .slick-next:before {
          color: #ff6b00; /* Orange arrow color */
          opacity: 1;
        }
        
        .slick-dots li button:before {
          color: #ff6b00; /* Match the dots color */
        }
        
        .slick-dots li.slick-active button:before {
          color: #ff6b00; /* Match the active dot color */
        }
      `}</style>
      <div className="mt-20">
        <Slider {...settings}>
        {events1.map((e, index) => {


            // Increment counter with each iteration
            const counter = index;

            // Logic to select different images based on counter
            let imageToShow;
            if (counter % 5 === 0) {
                imageToShow = "https://sfucsss.org/STATIC_URL/csss_static/logo.png"; // Assuming you have a field `image1`
            } else if (counter % 5 === 1) {
                imageToShow = "https://go.sfss.ca/clubs/831/logo"; // Assuming you have a field `image2`
            } else if (counter % 5 === 2) {
                imageToShow = "https://go.sfss.ca/clubs/676/logo"; // Default image
            } else if (counter % 5 === 3) {
                imageToShow = "https://go.sfss.ca/clubs/356/logo";
            } else if (counter % 5 === 4) {
                imageToShow = "https://go.sfss.ca/clubs/98/logo";
            }

            return (
          <div className="bg-green-200 text-black rounded-xl ">
            <div className="h-56 rounded-t-xl bg-blue-100 flex justify-center items-center">
                <img src = {imageToShow} alt="" className="h-44 w-44"/>
              </div>
              <div className="flex flex-col items-start gap-1 p-4 ">
                  <p className="text-xl font-semibold text-left font-bold">{e.name}</p>
                  <p className='text-left font-mono'>{"Date: " + e.startDate}</p>
                  <p className='text-left font-mono'>{"Starting time: " + e.start_time}</p>
                  <p className='text-left font-mono'>{"Ending time: " + e.end_time}</p>
                  <p className='text-left font-mono'>{"Location: " + e.location}</p>
                  <button className="bd-indigo-500 text-white text-lg px-6 py-0 rounded-xl"></button>
              </div>
          </div>
            );
        })}
        </Slider>
      </div>
    </div>

  );
};

export default EventScroller;