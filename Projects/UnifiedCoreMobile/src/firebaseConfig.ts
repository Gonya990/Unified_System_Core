import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { initializeAuth, signInAnonymously } from "firebase/auth";
// @ts-ignore
import { getReactNativePersistence } from "firebase/auth";
import { createAsyncStorage } from '@react-native-async-storage/async-storage';

const firebaseConfig = {
  projectId: "unified-core-agent-db",
  appId: "1:11800094827:web:6e990670a16761afa6692e",
  storageBucket: "unified-core-agent-db.firebasestorage.app",
  apiKey: "AIzaSyDCX3K2lYIkQk4JP5M1v1nbuWQ64kzNdWY",
  authDomain: "unified-core-agent-db.firebaseapp.com",
  messagingSenderId: "11800094827",
  projectNumber: "11800094827"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const appStorage = createAsyncStorage("unified-core");
export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(appStorage)
});

export const db = getFirestore(app);

// Authenticate device to get unique identity
signInAnonymously(auth).catch(console.error);
