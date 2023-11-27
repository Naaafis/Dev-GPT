import firebase from 'firebase/app';
import 'firebase/auth';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID
};

let firebaseApp;

try {
  if (!firebase.apps.length) {
    firebaseApp = firebase.initializeApp(firebaseConfig);
  } else {
    firebaseApp = firebase.app();
  }
} catch (error) {
  throw new Error('Firebase initialization error: ' + error.message);
}

const auth = firebaseApp.auth();

auth.setPersistence(firebase.auth.Auth.Persistence.LOCAL)
  .catch((error) => {
    throw new Error('Error setting persistence: ' + error.message);
  });

const signOut = () => {
  return auth.signOut()
    .catch((error) => {
      throw new Error('Error signing out: ' + error.message);
    });
};

const provider = new firebase.auth.GoogleAuthProvider();

const signInWithGoogle = () => {
  return auth.signInWithPopup(provider)
    .catch((error) => {
      throw new Error('Error signing in with Google: ' + error.message);
    });
};

export { auth, signOut, signInWithGoogle };