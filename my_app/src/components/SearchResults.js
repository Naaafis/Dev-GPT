import React from 'react';
import PropTypes from 'prop-types';

const SearchResults = ({ results, onResultSelect, loading, error }) => {
  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  if (results.length === 0) {
    return <p>No results found.</p>;
  }

  return (
    <ul>
      {results.map((result) => (
        <li key={result.id}>
          <button onClick={() => onResultSelect(result)}>
            {result.description}
          </button>
        </li>
      ))}
    </ul>
  );
};

SearchResults.propTypes = {
  results: PropTypes.array.isRequired,
  onResultSelect: PropTypes.func.isRequired,
  loading: PropTypes.bool,
  error: PropTypes.string,
};

export default SearchResults;
