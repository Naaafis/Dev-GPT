import React from 'react';
import styles from './SideBar.module.css'; // assuming you will create a SignIn.module.css


const SideBar = () => {
    return (
        <div class={styles.sideBar}>
        <a href="#" class={styles.box}><span>API Galore</span></a>
        <a href="#" class={styles.box}><span>Conversation</span></a>
        <a href="#" class={styles.box}><span>Gallery</span></a>
        <a href="#" class={styles.box}><span>Payment</span></a>
        <a href="#" class={styles.box}><span>Sign Out</span></a>
    </div>
    );
};

export default SideBar;
