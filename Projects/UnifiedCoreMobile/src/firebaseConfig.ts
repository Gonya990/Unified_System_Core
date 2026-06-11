/**
 * Firebase Configuration — SOVEREIGN SECURE
 * All credentials loaded from app.json extra (never hardcoded in source).
 * ✅ Security: No secrets in git-tracked source files.
 */
import Constants from 'expo-constants';
import { initializeApp, getApps, getApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { initializeAuth } from 'firebase/auth';
// @ts-ignore
import { getReactNativePersistence } from 'firebase/auth';
import { createAsyncStorage } from '@react-native-async-storage/async-storage';

// Read from app.json extra — injected at build time
const extra = Constants.expoConfig?.extra ?? {};
const fb = extra.firebase ?? {};

const firebaseConfig = {
  projectId:         fb.projectId         ?? 'unified-core-agent-db',
  appId:             fb.appId             ?? '',
  storageBucket:     fb.storageBucket     ?? '',
  apiKey:            fb.apiKey            ?? '',
  authDomain:        fb.authDomain        ?? '',
  messagingSenderId: fb.messagingSenderId ?? '',
};

// Prevent duplicate initialization (hot reload safe)
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

const appStorage = createAsyncStorage('unified-core');

export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(appStorage),
});

export const db = getFirestore(app);

// Authenticate device anonymously to get a unique identity
import { signInAnonymously, onAuthStateChanged } from 'firebase/auth';

export let deviceUserId: string | null = null;

onAuthStateChanged(auth, (user) => {
  if (user) {
    deviceUserId = user.uid;
  } else {
    signInAnonymously(auth).catch(console.error);
  }
});
