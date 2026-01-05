"use client"

import { useState } from "react"
import Image from "next/image"
import { Globe, Wifi, Building2, Smartphone, ArrowRight, ShieldCheck, Zap, BarChart3, Database, Sun, Moon, Languages } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { motion, AnimatePresence } from "framer-motion"

import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { ALL_LANGUAGES } from "@/app/data/languages"
import { TRAVEL_PHOTOS, OFFICE_PHOTOS } from "@/app/data/photos"

const translations = {
  ru: {
    nav: {
      coverage: "Покрытие",
      pricing: "Цены",
      tech: "Технология",
      api: "API"
    },
    hero: {
      b2c_tag: "Глобальный роуминг отменен",
      b2c_title_1: "Мир Твой.",
      b2c_title_2: "Просто подключись.",
      b2c_desc: "Мгновенный доступ к eSIM интернету в 190+ странах. Предоплаченные пакеты трафика без скрытых комиссий.",
      b2c_btn_1: "Найти страну",
      b2c_btn_2: "Скачать Приложение",
      b2b_tag: "Инфраструктура Трафика Класса Enterprise",
      b2b_title_1: "Масштабируемая",
      b2b_title_2: "Среда Связи.",
      b2b_desc: "Премиум трафик для бизнеса. API интеграция, выделенные каналы, оптовые пакеты данных и управление тысячами подключений.",
      b2b_btn_1: "Начать Интеграцию",
      b2b_btn_2: "Связаться с Sales"
    },
    stats: {
      countries: "Стран покрытия",
      speed: "Максимальная скорость",
      privacy: "Полная приватность",
      uptime: "Uptime гарантия"
    },
    pricing: {
      b2c_title: "Пакеты для Путешествий",
      b2c_subtitle: "Честные гигабайты на максимальной скорости. Неиспользованный трафик сгорает в конце срока, обеспечивая нам возможность держать лучшие цены.",
      b2b_title: "Инфраструктурные Тарифы",
      b2b_subtitle: "Оптовая закупка трафика. Подключайте своих пользователей через наш API. Вы платите за общий пул, ваши клиенты платят вам.",
      plans: {
        light: { name: "Light Tripper", desc: "Идеально для карт и мессенджеров на короткую поездку." },
        nomad: { name: "Digital Nomad", desc: "Хватит на звонки, работу и соцсети на целый месяц." },
        ultra: { name: "Ultra Stream", desc: "Максимум свободы. Стриминг, видео 4K и раздача интернета." },
        startup: { name: "Startup Pool", desc: "Для небольших команд и арбитраж-тестов." },
        agency: { name: "Agency Scale", desc: "Для маркетинговых агентств с большим расходом." },
        platform: { name: "Platform API", desc: "Интеграция в ваше приложение (White Label)." }
      },
      units: {
        pack: "пакет",
        month: "мес",
        days: "дней",
        instant: "Мгновенная активация (QR)",
        hidden_fees: "Без скрытых списаний",
        hotspot: "Разрешена раздача (Hotspot)",
        traffic: "Трафика",
        api_access: "API Ключ доступа",
        pool_ip: "Выделенный пул IP",
        pool_label: "TB Pool",
        select: "Выбрать",
        start: "Начать работу"
      }
    },
    footer: "Connect.Global © 2026. Все системы работают штатно."
  },
  en: {
    nav: {
      coverage: "Coverage",
      pricing: "Pricing",
      tech: "Technology",
      api: "API"
    },
    hero: {
      b2c_tag: "Global roaming is cancelled",
      b2c_title_1: "The World is Yours.",
      b2c_title_2: "Just Connect.",
      b2c_desc: "Instant access to eSIM internet in 190+ countries. Prepaid data packages with no hidden fees.",
      b2c_btn_1: "Find Country",
      b2c_btn_2: "Get the App",
      b2b_tag: "Enterprise Class Traffic Infrastructure",
      b2b_title_1: "Scalable",
      b2b_title_2: "Connectivity Env.",
      b2b_desc: "Premium traffic for business. API integration, dedicated channels, wholesale data packages, and management of thousands of connections.",
      b2b_btn_1: "Start Integration",
      b2b_btn_2: "Contact Sales"
    },
    stats: {
      countries: "Countries Covered",
      speed: "Max Speed",
      privacy: "Full Privacy",
      uptime: "Uptime Guarantee"
    },
    pricing: {
      b2c_title: "Travel Packages",
      b2c_subtitle: "Honest gigabytes at max speed. Unused traffic expires at the end of the term, allowing us to keep the best prices.",
      b2b_title: "Infrastructure Plans",
      b2b_subtitle: "Wholesale traffic purchase. Connect your users via our API. You pay for the shared pool, your clients pay you.",
      plans: {
        light: { name: "Light Tripper", desc: "Perfect for maps and messengers for a short trip." },
        nomad: { name: "Digital Nomad", desc: "Enough for calls, work, and social media for a whole month." },
        ultra: { name: "Ultra Stream", desc: "Maximum freedom. Streaming, 4K video, and hotspot tethering." },
        startup: { name: "Startup Pool", desc: "For small teams and arbitrage tests." },
        agency: { name: "Agency Scale", desc: "For marketing agencies with high consumption." },
        platform: { name: "Platform API", desc: "Integration into your app (White Label)." }
      },
      units: {
        pack: "pack",
        month: "mo",
        days: "days",
        instant: "Instant Activation (QR)",
        hidden_fees: "No hidden fees",
        hotspot: "Hotspot Allowed",
        traffic: "Traffic",
        api_access: "API Access Key",
        pool_ip: "Dedicated IP Pool",
        pool_label: "TB Pool",
        select: "Select",
        start: "Get Started"
      }
    },
    footer: "Connect.Global © 2026. All Systems Operational."
  }
}

export default function ConnectivityHub() {
  const [mode, setMode] = useState<"personal" | "business">("personal")
  const [lang, setLang] = useState("ru")
  const [langOpen, setLangOpen] = useState(false)
  const [theme, setTheme] = useState<"dark" | "light">("dark")

  const t = translations[lang as keyof typeof translations] || translations['en'] // Fallback to EN if translation missing

  // Theme logic
  const isDark = theme === 'dark'
  const bgClass = isDark ? "bg-black" : "bg-zinc-50"
  const textClass = isDark ? "text-white" : "text-zinc-900"
  const navBgClass = isDark ? "bg-black/50 border-white/5" : "bg-white/70 border-zinc-200"
  const cardBgClass = isDark ? "bg-zinc-900/50 border-white/5" : "bg-white border-zinc-200 shadow-lg"
  const mutedTextClass = isDark ? "text-zinc-400" : "text-zinc-500"
  const navTextClass = isDark ? "text-zinc-400 hover:text-white" : "text-zinc-600 hover:text-zinc-900"

  return (
    <div className={`min-h-screen ${bgClass} ${textClass} selection:bg-blue-500/30 font-sans transition-colors duration-500`}>
      {/* Navbar */}
      <nav className={`fixed top-0 w-full z-50 border-b backdrop-blur-xl transition-colors duration-500 ${navBgClass}`}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-blue-500" />
            <span className="font-bold text-xl tracking-tight">Connect<span className="text-blue-500">.Global</span></span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium">
            <a href="#stats" className={`${navTextClass} transition-colors`}>{t.nav.coverage}</a>
            <a href="#pricing" className={`${navTextClass} transition-colors`}>{t.nav.pricing}</a>
            <a href="#" className={`${navTextClass} transition-colors`}>{t.nav.tech}</a>
            <a href="#" className={`${navTextClass} transition-colors`}>{t.nav.api}</a>
          </div>
          <div className="flex items-center gap-4">
            <Popover open={langOpen} onOpenChange={setLangOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="ghost"
                  role="combobox"
                  aria-expanded={langOpen}
                  className={`w-[140px] justify-between ${navTextClass} text-xs uppercase tracking-wider font-bold hidden md:flex`}
                >
                  {lang === 'ru' ? 'Русский' : lang === 'en' ? 'English' : ALL_LANGUAGES.find(l => l.value === lang)?.label || lang}
                  <ChevronsUpDown className="ml-2 h-3 w-3 shrink-0 opacity-50" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-[200px] p-0 max-h-[400px]">
                <Command>
                  <CommandInput placeholder="Search language..." className="h-9" />
                  <CommandList>
                    <CommandEmpty>No language found.</CommandEmpty>
                    <CommandGroup className="max-h-[300px] overflow-y-auto">
                      {ALL_LANGUAGES.map((language) => (
                        <CommandItem
                          key={language.value}
                          value={language.label}
                          onSelect={() => {
                            setLang(language.value)
                            setLangOpen(false)
                          }}
                        >
                          {language.label}
                          <Check
                            className={cn(
                              "ml-auto h-4 w-4",
                              lang === language.value ? "opacity-100" : "opacity-0"
                            )}
                          />
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>

            {/* Mobile Lang Simplified (Icon only) */}
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="ghost" size="icon" className={`w-8 h-8 ${navTextClass} md:hidden`}>
                  <Languages className="w-4 h-4" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-[200px] p-0">
                <Command>
                  <CommandInput placeholder="Search..." className="h-9" />
                  <CommandList>
                    <CommandGroup className="max-h-[300px] overflow-y-auto">
                      {ALL_LANGUAGES.map((language) => (
                        <CommandItem
                          key={language.value}
                          value={language.label}
                          onSelect={() => {
                            setLang(language.value)
                          }}
                        >
                          {language.label}
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>

            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(isDark ? 'light' : 'dark')}
              className={`w-8 h-8 ${navTextClass}`}
            >
              {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </Button>

            <div className="w-px h-4 bg-zinc-700/50 mx-1"></div>

            <span className={`text-xs font-bold tracking-wider ${mode === 'personal' ? 'text-blue-500' : 'text-zinc-400'}`}>B2C</span>
            <Switch
              checked={mode === "business"}
              onCheckedChange={(c) => setMode(c ? "business" : "personal")}
              className="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-blue-600"
            />
            <span className={`text-xs font-bold tracking-wider ${mode === 'business' ? 'text-purple-500' : 'text-zinc-400'}`}>B2B</span>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative pt-32 pb-20 overflow-hidden">
        {/* Abstract Background */}
        <div className="absolute inset-0 z-0">
          <div className={`absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] rounded-full blur-[120px] opacity-20 transition-colors duration-1000 ${mode === 'personal' ? 'bg-blue-600' : 'bg-purple-600'}`} />
          <div
            className="absolute inset-0 opacity-[0.03]"
            style={{
              backgroundImage: `linear-gradient(${isDark ? '#fff' : '#000'} 1px, transparent 1px), linear-gradient(to right, ${isDark ? '#fff' : '#000'} 1px, transparent 1px)`,
              backgroundSize: '40px 40px'
            }}
          />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 text-center">
          <AnimatePresence mode="wait">
            <motion.div
              key={`${mode}-${lang}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="max-w-4xl mx-auto"
            >
              {mode === "personal" ? (
                <>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-500 text-xs mb-8">
                    <Wifi className="w-3 h-3" />
                    <span>{t.hero.b2c_tag}</span>
                  </div>
                  <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6">
                    {t.hero.b2c_title_1} <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
                      {t.hero.b2c_title_2}
                    </span>
                  </h1>
                  <p className={`text-xl ${mutedTextClass} mb-10 max-w-2xl mx-auto`}>
                    {t.hero.b2c_desc}
                  </p>
                  <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <Button
                      size="lg"
                      className="h-14 px-8 bg-blue-600 hover:bg-blue-500 rounded-full text-lg text-white"
                      onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })}
                    >
                      {t.hero.b2c_btn_1}
                      <ArrowRight className="ml-2 w-5 h-5" />
                    </Button>
                    <Button size="lg" variant="outline" className={`h-14 px-8 rounded-full text-lg ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}>
                      {t.hero.b2c_btn_2}
                    </Button>
                  </div>
                </>
              ) : (
                <>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-500 text-xs mb-8">
                    <Building2 className="w-3 h-3" />
                    <span>{t.hero.b2b_tag}</span>
                  </div>
                  <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6">
                    {t.hero.b2b_title_1} <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-300">
                      {t.hero.b2b_title_2}
                    </span>
                  </h1>
                  <p className={`text-xl ${mutedTextClass} mb-10 max-w-2xl mx-auto`}>
                    {t.hero.b2b_desc}
                  </p>
                  <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <Button
                      size="lg"
                      className="h-14 px-8 bg-purple-600 hover:bg-purple-500 rounded-full text-lg text-white"
                      onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })}
                    >
                      {t.hero.b2b_btn_1}
                      <Database className="ml-2 w-5 h-5" />
                    </Button>
                    <Button size="lg" variant="outline" className={`h-14 px-8 rounded-full text-lg ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}>
                      {t.hero.b2b_btn_2}
                    </Button>
                  </div>
                </>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Stats / Features Grid */}
      <section id="stats" className={`border-y ${isDark ? 'border-white/5 bg-white/5' : 'border-zinc-200 bg-zinc-100'} backdrop-blur-sm`}>
        <div className="max-w-7xl mx-auto px-6 py-12 grid grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="flex flex-col items-center text-center">
            <div className={`mb-4 p-3 rounded-2xl border ${isDark ? 'bg-zinc-900 border-white/10' : 'bg-white border-zinc-200 shadow-sm'}`}>
              <Globe className={`w-6 h-6 ${mutedTextClass}`} />
            </div>
            <div className="text-3xl font-bold mb-1">190+</div>
            <div className={`text-sm ${mutedTextClass}`}>{t.stats.countries}</div>
          </div>
          <div className="flex flex-col items-center text-center">
            <div className={`mb-4 p-3 rounded-2xl border ${isDark ? 'bg-zinc-900 border-white/10' : 'bg-white border-zinc-200 shadow-sm'}`}>
              <Zap className={`w-6 h-6 ${mutedTextClass}`} />
            </div>
            <div className="text-3xl font-bold mb-1">5G / LTE</div>
            <div className={`text-sm ${mutedTextClass}`}>{t.stats.speed}</div>
          </div>
          <div className="flex flex-col items-center text-center">
            <div className={`mb-4 p-3 rounded-2xl border ${isDark ? 'bg-zinc-900 border-white/10' : 'bg-white border-zinc-200 shadow-sm'}`}>
              <ShieldCheck className={`w-6 h-6 ${mutedTextClass}`} />
            </div>
            <div className="text-3xl font-bold mb-1">No KYC</div>
            <div className={`text-sm ${mutedTextClass}`}>{t.stats.privacy}</div>
          </div>
          <div className="flex flex-col items-center text-center">
            <div className={`mb-4 p-3 rounded-2xl border ${isDark ? 'bg-zinc-900 border-white/10' : 'bg-white border-zinc-200 shadow-sm'}`}>
              <BarChart3 className={`w-6 h-6 ${mutedTextClass}`} />
            </div>
            <div className="text-3xl font-bold mb-1">99.9%</div>
            <div className={`text-sm ${mutedTextClass}`}>{t.stats.uptime}</div>
          </div>
        </div>
      </section>

      {/* Marquee Section */}
      <div className="py-12 overflow-hidden bg-zinc-900 border-y border-white/5">
        <div className="flex gap-8 items-center animate-scroll whitespace-nowrap min-w-full" style={{
          maskImage: 'linear-gradient(to right, transparent, black 10%, black 90%, transparent)'
        }}>
          {/* Double the list for infinite scroll feel */}
          {[...(mode === 'personal' ? TRAVEL_PHOTOS : OFFICE_PHOTOS), ...(mode === 'personal' ? TRAVEL_PHOTOS : OFFICE_PHOTOS)].map((src, i) => (
            <motion.div
              key={i}
              className="w-[280px] h-[180px] flex-shrink-0 rounded-2xl overflow-hidden relative cursor-pointer group"
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05 }}
            >
              <div className={`absolute inset-0 transition-colors z-10 ${mode === 'personal' ? 'bg-blue-500/20' : 'bg-purple-500/20'} group-hover:bg-transparent`} />
              <Image
                src={src}
                alt="Connect User"
                fill
                className="object-cover group-hover:scale-110 transition-transform duration-700"
                sizes="(max-width: 768px) 280px, 280px"
              />
              <div className="absolute bottom-4 left-4 z-20 font-bold text-white text-sm drop-shadow-md">
                {mode === 'personal' ? 'Connect.Global Traveler' : 'Connect.Global Enterprise'}
              </div>
            </motion.div>
          ))}
        </div>
        {/* Simple CSS animation injection for marquee since tailwind config might not have it */}
        <style jsx>{`
            @keyframes scroll {
               from { transform: translateX(0); }
               to { transform: translateX(-50%); }
            }
            .animate-scroll {
               animation: scroll 180s linear infinite;
               width: max-content;
            }
            .animate-scroll:hover {
               animation-play-state: paused;
            }
         `}</style>
      </div>

      {/* Pricing / Packages */}
      <section id="pricing" className="py-24 max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">
            {mode === 'personal' ? t.pricing.b2c_title : t.pricing.b2b_title}
          </h2>
          <p className={`${mutedTextClass} max-w-2xl mx-auto`}>
            {mode === 'personal' ? t.pricing.b2c_subtitle : t.pricing.b2b_subtitle}
          </p>
        </div>

        <motion.div
          className="grid md:grid-cols-3 gap-6"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={{
            hidden: { opacity: 0 },
            visible: {
              opacity: 1,
              transition: { staggerChildren: 0.2 }
            }
          }}
        >
          {mode === 'personal' ? (
            // B2C CARDS
            <>
              {[
                { name: t.pricing.plans.light.name, price: 9, gb: 3, days: 7, icon: Smartphone, desc: t.pricing.plans.light.desc },
                { name: t.pricing.plans.nomad.name, price: 34, gb: 20, days: 30, icon: Globe, desc: t.pricing.plans.nomad.desc },
                { name: t.pricing.plans.ultra.name, price: 69, gb: 50, days: 30, icon: Zap, desc: t.pricing.plans.ultra.desc }
              ].map((plan, i) => (
                <motion.div
                  key={i}
                  variants={{
                    hidden: { opacity: 0, y: 30 },
                    visible: { opacity: 1, y: 0 }
                  }}
                  className={`group relative p-8 rounded-3xl ${cardBgClass} hover:border-blue-500/50 transition-all duration-300 hover:-translate-y-2`}
                >
                  <div className="absolute top-0 right-0 p-6 opacity-0 group-hover:opacity-100 transition-opacity">
                    <plan.icon className="w-8 h-8 text-blue-500" />
                  </div>
                  <h3 className={`text-xl font-bold mb-2`}>{plan.name}</h3>
                  <p className={`text-xs ${mutedTextClass} mb-6 h-8`}>{plan.desc}</p>

                  <div className="flex items-baseline gap-1 mb-6">
                    <span className={`text-5xl font-bold`}>${plan.price}</span>
                    <span className={`text-sm ${mutedTextClass}`}>/ {plan.days} {t.pricing.units.days}</span>
                  </div>

                  <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 mb-8">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-bold text-blue-500">{plan.gb} GB</span>
                      <span className="text-xs text-blue-400/70">Global Coverage</span>
                    </div>
                    <div className={`w-full ${isDark ? 'bg-zinc-800' : 'bg-zinc-200'} rounded-full h-1.5`}>
                      <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: `${(plan.gb / 50) * 100}%` }}></div>
                    </div>
                  </div>

                  <ul className={`space-y-3 mb-8 text-sm ${mutedTextClass}`}>
                    <li className="flex items-center gap-2">
                      <ShieldCheck className="w-4 h-4" />
                      <span>{t.pricing.units.instant}</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <ArrowRight className="w-4 h-4" />
                      <span>{t.pricing.units.hidden_fees}</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Wifi className="w-4 h-4" />
                      <span>{t.pricing.units.hotspot}</span>
                    </li>
                  </ul>
                  <Button className={`w-full h-12 font-bold transition-all ${isDark ? 'bg-white text-black hover:bg-blue-500 hover:text-white' : 'bg-black text-white hover:bg-blue-600'}`}>
                    {t.pricing.units.select} {plan.name}
                  </Button>
                </motion.div>
              ))}
            </>
          ) : (
            // B2B CARDS
            <>
              {[
                { name: t.pricing.plans.startup.name, price: 299, tb: 0.5, icon: Building2, desc: t.pricing.plans.startup.desc },
                { name: t.pricing.plans.agency.name, price: 999, tb: 2, icon: BarChart3, desc: t.pricing.plans.agency.desc },
                { name: t.pricing.plans.platform.name, price: 2499, tb: 10, icon: Database, desc: t.pricing.plans.platform.desc }
              ].map((plan, i) => (
                <motion.div
                  key={i}
                  variants={{
                    hidden: { opacity: 0, y: 30 },
                    visible: { opacity: 1, y: 0 }
                  }}
                  className={`group relative p-8 rounded-3xl ${cardBgClass} hover:border-purple-500/50 transition-all duration-300 hover:-translate-y-2`}
                >
                  <div className="absolute top-0 right-0 p-6 opacity-0 group-hover:opacity-100 transition-opacity">
                    <plan.icon className="w-8 h-8 text-purple-500" />
                  </div>
                  <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                  <p className={`text-xs ${mutedTextClass} mb-6 h-8`}>{plan.desc}</p>

                  <div className="flex items-baseline gap-1 mb-6">
                    <span className="text-5xl font-bold">${plan.price}</span>
                    <span className={`text-sm ${mutedTextClass}`}>/ {t.pricing.units.month}</span>
                  </div>

                  <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 mb-8">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-bold text-purple-500">{plan.tb} {t.pricing.units.pool_label}</span>
                      <span className="text-xs text-purple-400/70">~${(plan.price / (plan.tb * 1000)).toFixed(2)} / GB</span>
                    </div>
                    <div className={`w-full ${isDark ? 'bg-zinc-800' : 'bg-zinc-200'} rounded-full h-1.5`}>
                      <div className="bg-purple-500 h-1.5 rounded-full" style={{ width: `${(plan.price / 2500) * 100}%` }}></div>
                    </div>
                  </div>

                  <ul className={`space-y-3 mb-8 text-sm ${mutedTextClass}`}>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                      {/* B2B traffic calc */}
                      {plan.tb < 1 ? plan.tb * 1000 : plan.tb} {plan.tb < 1 ? 'GB' : 'TB'} {t.pricing.units.traffic}
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                      {t.pricing.units.api_access}
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                      {t.pricing.units.pool_ip}
                    </li>
                  </ul>
                  <Button className={`w-full h-12 font-bold transition-all ${isDark ? 'bg-zinc-800 hover:bg-purple-600 text-white border border-white/5' : 'bg-zinc-900 hover:bg-purple-600 text-white'}`}>
                    {t.pricing.units.start}
                  </Button>
                </motion.div>
              ))}
            </>
          )}
        </motion.div>
      </section >

      <footer className={`py-8 text-center text-sm ${mutedTextClass}`}>
        {t.footer}
      </footer>
    </div >
  )
}
