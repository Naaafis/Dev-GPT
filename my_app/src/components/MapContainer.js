import React from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';

export class MapContainer extends React.Component {
  render() {
    const { initialCenter = { lat: 47.444, lng: -122.176 }, zoom = 8, onError, options } = this.props;

    return (
      <div className="map-container">
        <Map
          google={this.props.google}
          zoom={zoom}
          initialCenter={initialCenter}
          onError={onError || ((error) => { console.error("Google Maps error:", error); })}
          {...options}
        />
      </div>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
})(MapContainer);