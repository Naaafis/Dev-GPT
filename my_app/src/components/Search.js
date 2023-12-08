import React, { useState } from 'react';
import PropTypes from 'prop-types';
import SearchResults from './SearchResults';

const Search = ({ onPlaceSelect }) => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // TODO: Implement the search functionality and update the results, loading, and error states.

  const handleResultSelect = (result) => {
    // Notify the parent component of the selected place.
    onPlaceSelect(result.place_id);
  };

  return (
    <div>
      <input type="text" placeholder="Search for places..." />
      <SearchResults results={results} onResultSelect={handleResultSelect} loading={loading} error={error} />
    </div>
  );
};

Search.propTypes = {
  onPlaceSelect: PropTypes.func.isRequired,
};

export default Search;
