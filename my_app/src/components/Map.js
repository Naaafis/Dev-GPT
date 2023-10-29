import React, { useEffect, useRef, useState } from 'react';
import MapControls from './MapControls';

const Map = () => {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);

  useEffect(() => {
    const initialMap = new window.google.maps.Map(mapRef.current, {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8,
    });
    setMap(initialMap);
  }, []);

  return (
    <div>
      <div ref={mapRef} style={{ height: '500px', width: '500px' }} />
      {map && <MapControls map={map} />}
    </div>
  );
};

export default Map;
