import React, { useState } from 'react';
import { fetchPlaces } from '../utils/api';
import '../styles/SearchBar.css'; // Ensure you import the CSS for styling

const SearchBar = ({ onPlacesFound, onError }) => {
    const [query, setQuery] = useState('');

    const handleSearchClick = async () => {
        console.log('Search button clicked, initiating search...');
        try {
            const places = await fetchPlaces(query);
            console.log('Fetched places:', places);
            onPlacesFound(places);
        } catch (error) {
            console.error('Error in handleSearchClick:', error);
            onError(error.message);
        }
    };

    const handleKeyDown = (event) => {
        console.log('Key pressed:', event.key);
        if (event.key === 'Enter') {
            handleSearchClick();
        }
    };

    return (
        <div className="search-container">
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                className="search-input"
                placeholder="Search for places..."
            />
            <button onClick={handleSearchClick} className="search-button">Search</button>
        </div>
    );
};

export default SearchBar;
