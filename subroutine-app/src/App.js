import React, { useEffect, useState } from 'react';
import SignIn from './components/SignIn';
import firebase from './firebase';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        setUser(user);
      } else {
        setUser(null);
      }
    });

    return () => unsubscribe();
  }, []);

  const signIn = async () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    await firebase.auth().signInWithPopup(provider);
  };

  const signOut = async () => {
    await firebase.auth().signOut();
  };

  return (
    <div>
      {user ? (
        <button onClick={signOut}>Sign Out</button>
      ) : (
        <SignIn signIn={signIn} />
      )}
    </div>
  );
}

export default App;
