"use client";

import { useState, useEffect } from "react";
import { auth } from "@/lib/firebaseConfig";
import { GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged, User } from "firebase/auth";
import { Button } from "./ui/button"; // Assuming standard shadcn button
import { LogIn, LogOut, User as UserIcon } from "lucide-react";

export default function AuthButton() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!auth) {
            requestAnimationFrame(() => setLoading(false));
            return;
        }
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            setUser(currentUser);
            setLoading(false);
        });
        return () => unsubscribe();
    }, []);

    const handleSignIn = async () => {
        if (!auth) return;
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
        } catch (error) {
            console.error("Error signing in:", error);
        }
    };

    const handleSignOut = async () => {
        if (!auth) return;
        try {
            await signOut(auth);
        } catch (error) {
            console.error("Error signing out:", error);
        }
    };

    if (loading) return <Button disabled variant="outline">Загрузка...</Button>;

    if (user) {
        return (
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full border border-white/20">
                    {user.photoURL ? (
                        <img src={user.photoURL} alt="User" className="w-6 h-6 rounded-full" />
                    ) : (
                        <UserIcon className="w-4 h-4" />
                    )}
                    <span className="text-sm font-medium text-white/90 truncate max-w-[100px]">
                        {user.displayName || user.email}
                    </span>
                </div>
                <Button
                    variant="outline"
                    onClick={handleSignOut}
                    className="bg-white/5 hover:bg-white/10 border-white/20 text-white"
                >
                    <LogOut className="w-4 h-4 mr-2" />
                    Выйти
                </Button>
            </div>
        );
    }

    return (
        <Button
            onClick={handleSignIn}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white border-none shadow-lg shadow-blue-500/20"
        >
            <LogIn className="w-4 h-4 mr-2" />
            Войти с Google
        </Button>
    );
}
