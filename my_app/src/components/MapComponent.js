import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Map, GoogleApiWrapper } from 'google-maps-react';

export class MapComponent extends Component {
  render() {
    if (!this.props.google) {
      return <div>Loading...</div>;
    }

    return (
      <Map
        google={this.props.google}
        zoom={14}
        initialCenter={{ lat: 47.444, lng: -122.176}}
      />
    );
  }
}

MapComponent.propTypes = {
  google: PropTypes.object.isRequired,
};

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
})(MapComponent);
