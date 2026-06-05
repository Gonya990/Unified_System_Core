"use client";

import Link from "next/link";
import { CheckCircle, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function SuccessPage() {
    return (
        <div className="min-h-screen bg-[#111418] flex items-center justify-center p-6 text-white font-sans">
            <div className="max-w-md w-full p-12 rounded-[40px] bg-white/5 border border-white/10 text-center shadow-2xl backdrop-blur-xl">
                <div className="w-20 h-20 rounded-full bg-green-500/20 flex items-center justify-center mx-auto mb-8 animate-bounce">
                    <CheckCircle className="w-10 h-10 text-green-500" />
                </div>
                <h1 className="text-4xl font-black mb-4 tracking-tighter">Оплата прошла успешно!</h1>
                <p className="text-zinc-400 mb-10 leading-relaxed">
                    Ваш баланс пополнен на 100 AI-кредитов. Теперь вы можете генерировать контент и получать торговые сигналы без ограничений.
                </p>
                <Link href="/">
                    <Button size="lg" className="w-full h-14 rounded-2xl bg-white text-black hover:bg-zinc-200 font-bold text-lg group">
                        Вернуться в Hub
                        <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                    </Button>
                </Link>
            </div>
        </div>
    );
}
