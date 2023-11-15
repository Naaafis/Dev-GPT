import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';

class Map extends Component {
  mapRef = React.createRef();

  componentDidMount() {
    this.loadMap();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.initialCenter !== this.props.initialCenter || prevProps.zoom !== this.props.zoom) {
      this.loadMap();
    }
  }

  loadMap() {
    const { google, initialCenter, zoom } = this.props;
    const maps = google.maps;

    const node = ReactDOM.findDOMNode(this.mapRef.current);

    const mapConfig = {
      center: initialCenter,
      zoom: zoom
    };

    try {
      new maps.Map(node, mapConfig);
    } catch (error) {
      console.error('Failed to create a new map instance: ', error);
    }
  }

  render() {
    return (
      <div ref={this.mapRef}>
        {this.props.loadingMessage}
      </div>
    );
  }
}

Map.propTypes = {
  google: PropTypes.object.isRequired,
  initialCenter: PropTypes.shape({
    lat: PropTypes.number,
    lng: PropTypes.number
  }).isRequired,
  zoom: PropTypes.number.isRequired,
  loadingMessage: PropTypes.string
};

Map.defaultProps = {
  initialCenter: { lat: 37.7749, lng: -122.4194 }, // Default coordinates (San Francisco)
  zoom: 10, // Default zoom level
  loadingMessage: 'Loading map...'
};

export default Map;
