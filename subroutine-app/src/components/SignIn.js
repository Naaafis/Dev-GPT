import React, { useState } from 'react';
import styles from '../style/SignIn.module.css';

const SignIn = ({ signIn }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSignIn = (event) => {
        event.preventDefault();
        signIn(email, password);
    };

    return (
        <div className={styles.a}>
            <div className={styles.b}>
                <p className={styles.c}>Login</p>
                <div className={styles.d}>
                    <input type="text" className={styles.e} placeholder="Login Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                    <input type="password" className={styles.e} placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    <div className={styles.f} onClick={handleSignIn}>GO</div> 
                </div>
                <div className={styles.g}>
                    Forget the password?<a href="#">Retrieve</a>
                </div>
            </div>
        </div>
    );
};

export default SignIn;
