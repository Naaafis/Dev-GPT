import React from 'react';

const MapControls = ({ map }) => {
  const handleZoomChange = (event) => {
    const zoomLevel = parseInt(event.target.value, 10);
    map.setZoom(zoomLevel);
  };

  const handleMapTypeChange = (event) => {
    const mapType = event.target.value;
    map.setMapTypeId(mapType);
  };

  return (
    <div className="map-controls">
      <label>
        Zoom:
        <input type="number" min="1" max="20" onChange={handleZoomChange} />
      </label>
      <label>
        Map Type:
        <select onChange={handleMapTypeChange}>
          <option value="roadmap">Roadmap</option>
          <option value="satellite">Satellite</option>
          <option value="hybrid">Hybrid</option>
          <option value="terrain">Terrain</option>
        </select>
      </label>
    </div>
  );
};

export default MapControls;
