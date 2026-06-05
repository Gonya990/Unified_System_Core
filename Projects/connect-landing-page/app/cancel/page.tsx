"use client";

import Link from "next/link";
import { XCircle, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function CancelPage() {
    return (
        <div className="min-h-screen bg-[#111418] flex items-center justify-center p-6 text-white font-sans">
            <div className="max-w-md w-full p-12 rounded-[40px] bg-white/5 border border-white/10 text-center shadow-2xl backdrop-blur-xl">
                <div className="w-20 h-20 rounded-full bg-red-500/20 flex items-center justify-center mx-auto mb-8">
                    <XCircle className="w-10 h-10 text-red-500" />
                </div>
                <h1 className="text-4xl font-black mb-4 tracking-tighter">Оплата отменена</h1>
                <p className="text-zinc-400 mb-10 leading-relaxed">
                    Процесс оплаты был прерван. Ваши средства не были списаны. Вы можете попробовать снова из личного кабинета.
                </p>
                <Link href="/">
                    <Button variant="outline" size="lg" className="w-full h-14 rounded-2xl border-white/10 hover:bg-white/5 text-white font-bold text-lg group">
                        <ArrowLeft className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
                        Вернуться назад
                    </Button>
                </Link>
            </div>
        </div>
    );
}
