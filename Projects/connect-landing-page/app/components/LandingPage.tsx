'use client';

import { useState } from 'react';
import { toast, Toaster } from 'sonner';
import { createOrder, type PlanType } from '@/lib/api';
import type { Destination } from '../data/destinations';

interface LandingPageProps {
    destinations: Destination[];
}

const PLAN_LABELS: Record<PlanType, string> = {
    explorer: 'Исследователь',
    connector: 'Коннектор',
    global_citizen: 'Гражданин Мира',
};

export default function LandingPage({ destinations }: LandingPageProps) {
    const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);
    const [selectedPlan, setSelectedPlan] = useState<PlanType | null>(null);
    const [customerName, setCustomerName] = useState('');
    const [customerEmail, setCustomerEmail] = useState('');
    const [isSubmittingPayment, setIsSubmittingPayment] = useState(false);

    const handleStartBridging = (e: React.MouseEvent) => {
        e.preventDefault();
        const pricingSection = document.getElementById('pricing');
        pricingSection?.scrollIntoView({ behavior: 'smooth' });
    };

    const openPayment = (plan: PlanType) => {
        setSelectedPlan(plan);
        setIsPaymentModalOpen(true);
    };

    const closePayment = () => {
        setIsPaymentModalOpen(false);
        setSelectedPlan(null);
        setCustomerName('');
        setCustomerEmail('');
        setIsSubmittingPayment(false);
    };

    const showError = (message: string) => {
        if (typeof window !== 'undefined' && toast?.error) {
            toast.error(message);
        } else {
            alert(message);
        }
    };

    const handlePayment = async (event: React.FormEvent) => {
        event.preventDefault();

        if (!selectedPlan) {
            return;
        }

        if (!customerName.trim() || !customerEmail.trim()) {
            showError('Введите имя и email для оплаты.');
            return;
        }

        setIsSubmittingPayment(true);

        try {
            const response = await createOrder(selectedPlan, {
                name: customerName.trim(),
                email: customerEmail.trim(),
            });

            if (!response?.payment_url) {
                throw new Error('Payment URL not returned.');
            }

            window.location.href = response.payment_url;
        } catch (error) {
            const message = error instanceof Error ? error.message : 'Failed to create payment order.';
            showError(message);
            setIsSubmittingPayment(false);
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground overflow-x-hidden selection:bg-primary selection:text-primary-foreground relative">
            <Toaster position="top-right" richColors />
            {/* Search / Hero Section */}
            <section className="relative h-[600px] flex flex-col items-center justify-center text-center px-4 overflow-hidden">
                {/* Dynamic Sky Background */}
                <div className="absolute inset-0 z-0 bg-gradient-to-b from-[var(--sky-gradient-start)] to-[var(--sky-gradient-end)] pointer-events-none">
                    <div className="absolute top-10 left-10 w-32 h-32 bg-white/20 rounded-full blur-3xl animate-float" />
                    <div className="absolute bottom-20 right-20 w-48 h-48 bg-white/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
                </div>

                <div className="relative z-10 max-w-2xl space-y-6">
                    <h1 className="text-5xl md:text-7xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-br from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">
                        Мы соединяем вас.
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 font-light">
                        Преодолевая расстояния, создавая отношения.
                    </p>

                    <form className="w-full max-w-md mx-auto flex gap-2 mt-8" role="search" aria-label="Найти связь" onSubmit={(e) => e.preventDefault()}>
                        <input
                            type="text"
                            placeholder="Где вы хотите найти своих?"
                            className="flex-1 px-6 py-4 rounded-full border border-gray-200 dark:border-gray-800 bg-card text-card-foreground shadow-lg focus:outline-none focus:ring-2 focus:ring-primary transition-all"
                            aria-label="Поиск направления"
                        />
                        <button
                            type="button"
                            onClick={handleStartBridging}
                            className="px-8 py-4 bg-primary text-primary-foreground rounded-full font-medium hover:opacity-90 transition-opacity shadow-lg"
                            aria-label="Найти"
                        >
                            Найти
                        </button>
                    </form>
                </div>
            </section>

            {/* Destinations Section */}
            <section className="py-24 px-4 bg-gray-50 dark:bg-zinc-900/50">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-3xl font-bold mb-12 text-center">Популярные направления</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {destinations.map((dest) => (
                            <div
                                key={dest.id}
                                className="group p-6 rounded-2xl bg-card border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-md transition-all hover:-translate-y-1 duration-300"
                            >
                                <div className="flex items-start justify-between mb-4">
                                    <div className="text-4xl">{dest.flag}</div>
                                    <span className="text-sm font-medium px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400">
                                        Активный хаб
                                    </span>
                                </div>
                                <h3 className="text-xl font-bold mb-2">{dest.city}, {dest.country}</h3>
                                <p className="text-gray-500 dark:text-gray-400 leading-relaxed">
                                    {dest.description}
                                </p>
                                <button
                                    onClick={handleStartBridging}
                                    className="mt-6 text-sm font-semibold text-primary hover:underline underline-offset-4 flex items-center gap-1 cursor-pointer"
                                    aria-label={`Соединиться с ${dest.city}`}
                                >
                                    Начать общение <span>&rarr;</span>
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Pricing Section (NEW) */}
            <section id="pricing" className="py-24 px-4 bg-background">
                <div className="max-w-6xl mx-auto text-center">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4">Выберите свой путь</h2>
                    <p className="text-xl text-gray-500 dark:text-gray-400 mb-16">Откройте мир с нашими гибкими планами.</p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Basic Plan */}
                        <div className="p-8 rounded-3xl border border-gray-200 dark:border-gray-800 hover:border-blue-500 transition-colors flex flex-col justify-between">
                            <div>
                                <h3 className="text-2xl font-bold mb-2">Исследователь</h3>
                                <div className="text-4xl font-bold mb-6">$0 <span className="text-lg font-normal text-gray-500">/мес</span></div>
                                <ul className="text-left space-y-4 mb-8 text-gray-600 dark:text-gray-300">
                                    <li className="flex items-center gap-2">✓ Доступ к форумам сообщества</li>
                                    <li className="flex items-center gap-2">✓ Базовые гиды по городам</li>
                                    <li className="flex items-center gap-2">✓ 1 запрос на подключение/мес</li>
                                </ul>
                            </div>
                            <button
                                onClick={() => openPayment('explorer')}
                                className="w-full py-4 rounded-xl border-2 border-primary text-primary font-bold hover:bg-primary hover:text-white transition-all"
                            >
                                Выбрать Исследователя
                            </button>
                        </div>

                        {/* Pro Plan */}
                        <div className="p-8 rounded-3xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-2xl scale-105 relative transform">
                            <div className="absolute top-0 right-0 bg-yellow-400 text-black text-xs font-bold px-3 py-1 rounded-bl-xl rounded-tr-3xl">ПОПУЛЯРНЫЙ</div>
                            <div>
                                <h3 className="text-2xl font-bold mb-2">Коннектор</h3>
                                <div className="text-4xl font-bold mb-6">$29 <span className="text-lg font-normal text-blue-200">/мес</span></div>
                                <ul className="text-left space-y-4 mb-8 text-blue-50">
                                    <li className="flex items-center gap-2">✓ Безлимитные сообщения</li>
                                    <li className="flex items-center gap-2">✓ Премиум гиды по городам</li>
                                    <li className="flex items-center gap-2">✓ Безлимитные запросы</li>
                                    <li className="flex items-center gap-2">✓ Приоритетная поддержка</li>
                                </ul>
                            </div>
                            <button
                                onClick={() => openPayment('connector')}
                                className="w-full py-4 rounded-xl bg-white text-blue-600 font-bold hover:bg-gray-100 transition-all shadow-lg"
                            >
                                Подключиться
                            </button>
                        </div>

                        {/* Enterprise Plan */}
                        <div className="p-8 rounded-3xl border border-gray-200 dark:border-gray-800 hover:border-purple-500 transition-colors flex flex-col justify-between">
                            <div>
                                <h3 className="text-2xl font-bold mb-2">Гражданин Мира</h3>
                                <div className="text-4xl font-bold mb-6">$99 <span className="text-lg font-normal text-gray-500">/мес</span></div>
                                <ul className="text-left space-y-4 mb-8 text-gray-600 dark:text-gray-300">
                                    <li className="flex items-center gap-2">✓ Все возможности Коннектора</li>
                                    <li className="flex items-center gap-2">✓ Личный агент по переезду</li>
                                    <li className="flex items-center gap-2">✓ Юридическая и визовая помощь</li>
                                    <li className="flex items-center gap-2">✓ Закрытые мероприятия</li>
                                </ul>
                            </div>
                            <button
                                onClick={() => openPayment('global_citizen')}
                                className="w-full py-4 rounded-xl border-2 border-gray-300 dark:border-gray-700 font-bold hover:border-primary hover:text-primary transition-all"
                            >
                                Выбрать Global
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-12 text-center text-sm text-gray-500 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-zinc-900">
                <p>© 2026 Connect Inc. Объединяя мир.</p>
                <div className="mt-4 space-x-4">
                    <a href="#" className="hover:text-primary transition-colors">Политика</a>
                    <a href="#" className="hover:text-primary transition-colors">Условия</a>
                    <a href="#" className="hover:text-primary transition-colors">Доступность</a>
                </div>
            </footer>

            {/* Payment Modal Overlay */}
            {isPaymentModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
                    <div className="bg-white dark:bg-zinc-900 w-full max-w-lg rounded-3xl shadow-2xl p-8 relative animate-in zoom-in-95 duration-200">
                        <button
                            onClick={closePayment}
                            disabled={isSubmittingPayment}
                            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>

                        <h3 className="text-2xl font-bold mb-2">
                            Подтвердить: {selectedPlan ? PLAN_LABELS[selectedPlan] : ''}
                        </h3>
                        <p className="text-gray-500 mb-8">Введите имя и email, чтобы перейти к оплате.</p>

                        <form className="space-y-6" onSubmit={handlePayment}>
                            <div>
                                <label className="block text-sm font-medium mb-2">Имя</label>
                                <input
                                    type="text"
                                    placeholder="Ваше имя"
                                    value={customerName}
                                    onChange={(event) => setCustomerName(event.target.value)}
                                    disabled={isSubmittingPayment}
                                    className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-zinc-800 focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:opacity-70"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-2">Email</label>
                                <input
                                    type="email"
                                    placeholder="you@example.com"
                                    value={customerEmail}
                                    onChange={(event) => setCustomerEmail(event.target.value)}
                                    disabled={isSubmittingPayment}
                                    className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-zinc-800 focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:opacity-70"
                                />
                            </div>

                            <button
                                type="submit"
                                disabled={isSubmittingPayment}
                                className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-500/30 disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {isSubmittingPayment ? (
                                    <span className="inline-flex items-center justify-center gap-2">
                                        <span className="h-4 w-4 rounded-full border-2 border-white/70 border-t-transparent animate-spin" />
                                        Перенаправляем...
                                    </span>
                                ) : (
                                    'Перейти к оплате'
                                )}
                            </button>
                        </form>

                        <div className="mt-6 text-center text-xs text-gray-400">
                            <p>🔒 256-битное SSL шифрование</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
