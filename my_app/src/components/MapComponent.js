import React from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';

class MapComponent extends React.Component {
  render() {
    const { lat, lng, google } = this.props;
    const coordinates = { lat: lat || 47.444, lng: lng || -122.176 };

    return (
      <Map
        google={google}
        zoom={14}
        initialCenter={coordinates}
        onError={(err) => {
          // Handle map loading errors here
          console.error('Error loading map', err);
        }}
      />
    );
  }
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
})(MapComponent);
