import React from "react";
import "./map.css";

function Map() {
    return (
        <div className="map-container">
            <iframe
                title="Map"
                width="2000"
                height="2000"
                style={{ border: 0 }}
                loading="lazy"
                allowFullScreen
                src="https://www.google.com/maps/embed/v1/place?key=AIzaSyCt75JP2DkIq4NVesfAYmB6HuJQ6zF3vEo&q=Space+Needle,Seattle+WA">
            </iframe>
        </div>
    );
}

export default Map;