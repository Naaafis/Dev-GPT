import React from 'react';
import styles from './index_MainBanner.module.css'; // assuming the CSS is in the same directory

const MainBanner = () => {
  return (
    <div className={styles.mainBanner}>
        <img src="https://fakeimg.pl/1920x3080" alt="Banner Image" className={styles.bannerImage} />
        <div className={styles.bannerContent}>
            <h1 className={styles.bannerHeader}>Build Your Dreams With Us</h1>
            <h2 className={styles.bannerSubheadline}>Connecting You with Skilled Craftsmen</h2>
            <p className={styles.bannerText}> {/* Additional text content goes here */} </p>
        </div>
    </div>
  );
};

export default MainBanner;
