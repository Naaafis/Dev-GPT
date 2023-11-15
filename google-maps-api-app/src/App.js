import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import MapWithWrapper from './components/MapWithWrapper';
import { fetchDirections, getUserLocation } from './utils/api'; // make sure to export getUserLocation from api.js

const App = () => {
  const [directions, setDirections] = useState(null);
  const [center, setCenter] = useState({ lat: -34.397, lng: 150.644 }); // Default center, should be updated with user's location
  const [zoom, setZoom] = useState(8);

  // Function to handle when a destination is selected from the search bar
  const handlePlaceSelect = async (place) => {
    const destination = place.geometry.location; // Extract the destination from the selected place
    try {
      const userLocation = await getUserLocation(); // Assuming this function is implemented to get the user's current location
      fetchDirections(userLocation, destination, setDirections); // Fetch directions using the utility function
    } catch (error) {
      console.error('Error getting user location or fetching directions:', error);
    }
  };

  // Function passed to the SearchBar and called when a place is found
  const handlePlacesFound = (places) => {
    if (places.length > 0) {
      handlePlaceSelect(places[0]); // For simplicity, automatically select the first place found
    }
  };

  const handleError = (error) => {
    console.error(error);
  };

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <SearchBar onPlacesFound={handlePlacesFound} onError={handleError} />
      <MapWithWrapper center={center} zoom={zoom} directions={directions} />
    </div>
  );
};

export default App;
