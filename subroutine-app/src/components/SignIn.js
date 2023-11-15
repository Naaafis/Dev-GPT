import React from 'react';
import styles from '../style/SignIn.module.css'; // assuming you will create a SignIn.module.css

const SignIn = () => {
    return (
        <div className={styles.a}>
            <div className={styles.b}>
                <p className={styles.c}>Login</p>
                <div className={styles.d}>
                    <input type="text" className={styles.e} placeholder="Login Email" />
                    <input type="password" className={styles.e} placeholder="Password" />
                    <div className={styles.f}>GO</div>
                </div>
                <div className={styles.g}>
                    Forget the password?<a href="#">Retrieve</a>
                </div>
            </div>
        </div>
    );
};

export default SignIn;