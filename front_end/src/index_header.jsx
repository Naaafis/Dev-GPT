import React from 'react';
import styles from './Image_header.module.css'; // assuming the CSS is in the same directory

const Header = () => {
  return (
    <nav className={styles.navbar}>
        <div className={styles.logo}>BuilderHire</div>
        <div className={styles.navLinks}>
            <a href="#">Homepage</a>
            <a href="#">Worker Profiles</a>
            <a href="#">Projects</a>
            {/* Additional links as seen in design */}
        </div>
        <div className={styles.search}>
            <input type="text" placeholder="Search..." />
        </div>
    </nav>
  );
};

export default Header;
