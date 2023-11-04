import React, { useRef, useEffect } from 'react';
import { Wrapper, Status } from '@googlemaps/react-wrapper';


const MapComponent = ({ center, zoom, directions }) => {
    const ref = useRef();

    useEffect(() => {
        const map = new window.google.maps.Map(ref.current, {
            center,
            zoom,
        });

        if (directions) {
            const directionsRenderer = new window.google.maps.DirectionsRenderer();
            directionsRenderer.setMap(map);
            directionsRenderer.setDirections(directions);
        }

    }, [center, zoom, directions]);

    return <div ref={ref} id="map" style={{ width: '100%', height: '100%' }} />;
};

const MapWithWrapper = ({ center, zoom, directions }) => {
    return (
        <Wrapper apiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY} render={status => {
            if (status === Status.LOADING) return <div>Loading...</div>;
            if (status === Status.FAILURE) return <div>Error loading maps</div>;
            return <MapComponent center={center} zoom={zoom} directions={directions} />;
        }} />
    );
};

export default MapWithWrapper;
