import React, { useState } from 'react';
import styles from './Directions.module.css';

const Directions = () => {
  const [startLocation, setStartLocation] = useState('');
  const [endLocation, setEndLocation] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // TODO: Implement the logic to call the Google Maps Directions service
    // For now, we'll just log the start and end locations
    console.log('Form submitted with start location:', startLocation, 'and end location:', endLocation);
    // Reset error message
    setError('');
  };

  return (
    <div className={styles.formContainer}>
      <h2>Get Directions</h2>
      <form onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="startLocation" className={styles.label}>Start Location:</label>
          <input
            type="text"
            id="startLocation"
            className={styles.input}
            value={startLocation}
            onChange={(e) => setStartLocation(e.target.value)}
            placeholder="Enter start location"
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="endLocation" className={styles.label}>End Location:</label>
          <input
            type="text"
            id="endLocation"
            className={styles.input}
            value={endLocation}
            onChange={(e) => setEndLocation(e.target.value)}
            placeholder="Enter end location"
          />
        </div>
        <button type="submit" className={styles.submitButton}>Get Directions</button>
        {error && <p className={styles.error}>{error}</p>}
      </form>
    </div>
  );
};

export default Directions;
