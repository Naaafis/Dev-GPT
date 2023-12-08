import React, { useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * Marker component.
 * This component uses the Google Maps JavaScript API to create a new marker instance.
 * @param {Object} props - The props of the component.
 * @param {google.maps.Map} props.map - The map instance.
 * @param {Object} props.google - The google object from the Google Maps JavaScript API.
 * @param {Object} props.position - The position of the marker.
 * @param {string} props.title - The title of the marker.
 */
const Marker = ({ map, google, position, title }) => {
  useEffect(() => {
    try {
      const marker = new google.maps.Marker({
        position,
        map,
        title
      });

      return () => {
        marker.setMap(null);
      };
    } catch (error) {
      console.error('Failed to create marker:', error);
    }
  }, [map, google, position, title]);

  return null;
};

Marker.propTypes = {
  map: PropTypes.object.isRequired,
  google: PropTypes.object.isRequired,
  position: PropTypes.shape({
    lat: PropTypes.number.isRequired,
    lng: PropTypes.number.isRequired
  }).isRequired,
  title: PropTypes.string
};

Marker.defaultProps = {
  title: ''
};

export default Marker;
