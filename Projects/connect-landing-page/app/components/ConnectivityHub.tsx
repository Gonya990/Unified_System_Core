"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import {
  Globe, Wifi, Building2, Smartphone, ArrowRight, ShieldCheck, Zap,
  BarChart3, Database, Sun, Moon, Languages, Quote, Phone,
  CreditCard, CheckCircle, Download, User, Settings, Star,
  Check, ChevronsUpDown
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { motion, AnimatePresence } from "framer-motion"

import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { cn } from "@/lib/utils"

import { ALL_LANGUAGES } from "@/app/data/languages"
import { TRAVEL_PHOTOS, OFFICE_PHOTOS } from "@/app/data/photos"
import { TOP_COUNTRIES } from "@/app/data/countries"
import { translations, type Translation } from "@/app/data/translations"

interface Plan {
  name: string;
  price: string;
  desc: string;
  features: string[];
}

export default function ConnectivityHub() {
  const [mode, setMode] = useState<"personal" | "business">("personal")
  const [lang, setLang] = useState("ru")
  const [langOpen, setLangOpen] = useState(false)
  const [langMobileOpen, setLangMobileOpen] = useState(false)
  const [theme, setTheme] = useState<"dark" | "light">("dark")
  const [isDetected, setIsDetected] = useState(false)
  const [dataVal, setDataVal] = useState(500)
  const [selectedCountry, setSelectedCountry] = useState("")
  const [countryOpen, setCountryOpen] = useState(false)

  // Plan Config & Checkout
  const [activePlan, setActivePlan] = useState<Plan | null>(null)
  const [checkoutStep, setCheckoutStep] = useState<"config" | "payment" | "success" | null>(null)
  const [customGB, setCustomGB] = useState(5)
  const [customMins, setCustomMins] = useState(100)
  const [hasSMS, setHasSMS] = useState(false)

  const t: Translation = translations[lang] || translations['en']

  // Handle plan selection and initial config
  const handleSelectPlan = (plan: Plan) => {
    setActivePlan(plan)
    if (plan.name.includes("Light")) {
      setCustomGB(3)
      setCustomMins(100)
      setHasSMS(false)
    } else if (plan.name.includes("Nomad")) {
      setCustomGB(15)
      setCustomMins(300)
      setHasSMS(false)
    } else if (plan.name.includes("Ultra")) {
      setCustomGB(50)
      setCustomMins(1000)
      setHasSMS(true)
    } else {
      setCustomGB(5)
      setCustomMins(150)
      setHasSMS(false)
    }
    setCheckoutStep("config")
  }

  const calculateTotal = () => {
    if (!activePlan) return 0
    const base = parseFloat(activePlan.price.replace('$', ''))
    // Logic for extra data: $2 per GB, $0.05 per Min, $5 for SMS
    const baseGB = activePlan.name.includes("Light") ? 3 : activePlan.name.includes("Nomad") ? 15 : 50
    const extraGB = Math.max(0, customGB - baseGB)
    const extraMins = Math.max(0, customMins - 100)
    return base + (extraGB * 2) + (extraMins * 0.05) + (hasSMS ? 5 : 0)
  }

  useEffect(() => {
    const timer = setTimeout(() => setIsDetected(true), 2500)
    return () => clearTimeout(timer)
  }, [])

  // Theme logic
  const isDark = theme === 'dark'
  const bgClass = isDark ? "bg-[#0a0c10]" : "bg-[#fcfaf2]" // Soft Midnight Black vs Warm Beige
  const textClass = isDark ? "text-zinc-100" : "text-stone-900"
  const navBgClass = isDark ? "bg-[#0a0c10]/80 border-white/5" : "bg-[#fcfaf2]/80 border-stone-200"
  const cardBgClass = isDark ? "bg-zinc-900/40 border-white/5" : "bg-white/90 border-stone-100 shadow-sm"
  const mutedTextClass = isDark ? "text-zinc-400" : "text-stone-500"
  const navTextClass = isDark ? "text-zinc-400 hover:text-zinc-100" : "text-stone-600 hover:text-stone-900"
  const isRTL = lang === 'he' || lang === 'ar' || lang === 'fa'

  return (
    <div
      dir={isRTL ? "rtl" : "ltr"}
      className={`min-h-screen ${bgClass} ${textClass} selection:bg-blue-500/30 font-sans transition-colors duration-500`}
    >
      {/* Navbar */}
      <nav className={`fixed top-0 w-full z-50 border-b backdrop-blur-xl transition-colors duration-500 ${navBgClass}`}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Globe className={`w-5 h-5 transition-colors duration-500 ${mode === 'personal' ? 'text-blue-500' : 'text-purple-500'}`} />
            <span className="font-bold text-xl tracking-tight relative">
              Connect
              <span className={`transition-colors duration-500 ${mode === 'personal' ? 'text-blue-500' : 'text-purple-500'}`}>.Global</span>
              {mode === 'business' && (
                <motion.div
                  layoutId="glow"
                  className="absolute -inset-1 bg-purple-500/20 blur-sm rounded-lg -z-10"
                />
              )}
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium">
            <a href="#stats" className={`${navTextClass} transition-colors`}>{t.nav.coverage}</a>
            <a href="#pricing" className={`${navTextClass} transition-colors`}>{t.nav.pricing}</a>
            <a href="#app" className={`${navTextClass} transition-colors`}>{t.nav.tech}</a>
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
                  <ChevronsUpDown className="ms-2 h-3 w-3 shrink-0 opacity-50" />
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
                          value={language.value}
                          onSelect={(currentValue) => {
                            setLang(currentValue)
                            setLangOpen(false)
                          }}
                        >
                          <Check
                            className={cn(
                              "me-2 h-4 w-4",
                              lang === language.value ? "opacity-100" : "opacity-0"
                            )}
                          />
                          {language.label}
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>

            <Popover open={langMobileOpen} onOpenChange={setLangMobileOpen}>
              <PopoverTrigger asChild>
                <Button variant="ghost" size="icon" className={`md:hidden ${navTextClass}`}>
                  <Languages className="w-5 h-5" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-[200px] p-0 max-h-[400px]">
                <Command>
                  <CommandInput placeholder="Search language..." className="h-9" />
                  <CommandList>
                    <CommandGroup className="max-h-[300px] overflow-y-auto">
                      {ALL_LANGUAGES.map((language) => (
                        <CommandItem
                          key={language.value}
                          value={language.value}
                          onSelect={(currentValue) => {
                            setLang(currentValue)
                            setLangMobileOpen(false)
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

                  <div className="flex flex-col items-center gap-6">
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full max-w-2xl">
                      <Popover open={countryOpen} onOpenChange={setCountryOpen}>
                        <PopoverTrigger asChild>
                          <Button
                            size="lg"
                            className="h-14 px-8 bg-blue-600 hover:bg-blue-500 rounded-full text-lg text-white w-full sm:w-[320px] justify-between group overflow-hidden relative"
                          >
                            <span className="flex items-center gap-2">
                              <Globe className="w-5 h-5 group-hover:rotate-12 transition-transform" />
                              {selectedCountry || t.hero.b2c_btn_1}
                            </span>
                            <ArrowRight className="ms-2 w-5 h-5 opacity-50 group-hover:translate-x-1 transition-transform" />
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className={`w-[320px] p-0 ${isDark ? 'bg-zinc-900 border-white/10' : 'bg-white border-zinc-200'}`} align="center">
                          <Command className={isDark ? 'bg-zinc-900' : 'bg-white'}>
                            <CommandInput placeholder={t.hero.search_placeholder} className="h-12" />
                            <CommandList className="max-h-[300px]">
                              <CommandEmpty>No country found.</CommandEmpty>
                              <CommandGroup>
                                {TOP_COUNTRIES.map((c) => (
                                  <CommandItem
                                    key={c.code}
                                    value={c.name}
                                    onSelect={() => {
                                      setSelectedCountry(`${c.flag} ${c.name}`);
                                      setCountryOpen(false);
                                      document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' });
                                    }}
                                    className="flex items-center gap-3 py-3 cursor-pointer"
                                  >
                                    <span className="text-xl">{c.flag}</span>
                                    <div className="flex flex-col">
                                      <span className="font-medium">{c.name}</span>
                                      <span className="text-xs opacity-50">{c.region}</span>
                                    </div>
                                  </CommandItem>
                                ))}
                              </CommandGroup>
                            </CommandList>
                          </Command>
                        </PopoverContent>
                      </Popover>

                      <Button size="lg" variant="outline" className={`h-14 px-8 rounded-full text-lg w-full sm:w-auto ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}>
                        {t.hero.b2c_btn_2}
                      </Button>
                    </div>

                    {/* Popular Destinations Chips */}
                    <div className="flex flex-wrap justify-center gap-2 max-w-3xl">
                      <span className={`text-xs font-bold uppercase tracking-widest ${mutedTextClass} w-full mb-2`}>
                        {t.hero.popular_dest}
                      </span>
                      {TOP_COUNTRIES.slice(0, 10).map((c) => (
                        <button
                          key={c.code}
                          onClick={() => {
                            setSelectedCountry(`${c.flag} ${c.name}`);
                            document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' });
                          }}
                          className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-medium transition-all hover:scale-105 active:scale-95 ${isDark ? 'bg-zinc-900 border-white/5 hover:border-blue-500/50 hover:bg-blue-500/10' : 'bg-white border-zinc-200 hover:border-blue-500/50 hover:bg-blue-50/50'}`}
                        >
                          <span>{c.flag}</span>
                          <span>{c.name}</span>
                        </button>
                      ))}
                    </div>

                    <div className="mt-4 flex flex-col items-center">
                      <div className={`flex items-center gap-3 px-4 py-2 rounded-2xl border transition-all duration-1000 ${isDetected ? (isDark ? 'bg-green-500/10 border-green-500/30' : 'bg-green-50 border-green-200') : (isDark ? 'bg-zinc-800 border-white/5' : 'bg-zinc-100 border-zinc-200')}`}>
                        {!isDetected ? (
                          <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                          >
                            <Globe className={`w-4 h-4 ${isDark ? 'text-zinc-500' : 'text-zinc-400'}`} />
                          </motion.div>
                        ) : (
                          <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}>
                            <div className="w-4 h-4 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]" />
                          </motion.div>
                        )}
                        <span className={`text-sm font-medium ${isDetected ? (isDark ? 'text-green-400' : 'text-green-600') : mutedTextClass}`}>
                          {isDetected ? `${t.hero.loc_found}` : t.hero.loc_detecting}
                        </span>
                        {isDetected && (
                          <motion.span
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="font-bold text-sm bg-blue-500 px-2 py-0.5 rounded text-white"
                          >
                            15GB / $29
                          </motion.span>
                        )}
                      </div>
                    </div>
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
                    <Button size="lg" className="h-14 px-8 bg-purple-600 hover:bg-purple-500 rounded-full text-lg text-white">
                      {t.hero.b2b_btn_1}
                      <ArrowRight className="ms-2 w-5 h-5" />
                    </Button>
                    <Button size="lg" variant="outline" className={`h-14 px-8 rounded-full text-lg ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}>
                      {t.hero.b2b_btn_2}
                    </Button>
                  </div>

                  {/* B2B Dashboard Mockup */}
                  <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className={`mt-20 p-8 rounded-[32px] border ${cardBgClass} max-w-5xl mx-auto overflow-hidden relative group`}
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />
                    <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 mb-12 relative z-10">
                      <div className="text-start">
                        <h3 className="text-2xl font-bold mb-2">{t.dashboard.title}</h3>
                        <div className="flex items-center gap-2 text-green-500 text-sm font-medium">
                          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                          {t.dashboard.status}
                        </div>
                      </div>
                      <div className={`flex items-center gap-4 px-4 py-2 rounded-2xl bg-white/5 border border-white/5 backdrop-blur-md`}>
                        <ShieldCheck className="w-5 h-5 text-purple-400" />
                        <span className="text-xs font-bold tracking-tight opacity-70 uppercase">{t.dashboard.israel_optimized}</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
                      {[
                        { label: t.dashboard.nodes, val: "1,284", icon: Globe, color: "text-blue-400" },
                        { label: t.dashboard.traffic, val: "4.2 Tbps", icon: Zap, color: "text-purple-400" },
                        { label: t.dashboard.latency, val: "12ms", icon: BarChart3, color: "text-pink-400" }
                      ].map((stat, i) => (
                        <div key={i} className={`p-6 rounded-2xl bg-white/5 border border-white/5 text-start hover:bg-white/10 transition-colors`}>
                          <stat.icon className={`w-5 h-5 mb-4 ${stat.color}`} />
                          <div className={`text-[10px] ${mutedTextClass} mb-1 uppercase font-black tracking-widest`}>{stat.label}</div>
                          <div className="text-2xl font-bold">{stat.val}</div>
                        </div>
                      ))}
                    </div>

                    {/* Simple Sparkline Chart Mockup */}
                    <div className="mt-8 h-32 w-full relative group">
                      <svg className="w-full h-full opacity-30 transition-opacity group-hover:opacity-50" viewBox="0 0 1000 100">
                        <motion.path
                          d="M0,50 Q100,20 200,80 T400,40 T600,60 T800,20 T1000,50"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="3"
                          className="text-purple-500"
                          initial={{ pathLength: 0 }}
                          animate={{ pathLength: 1 }}
                          transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
                        />
                      </svg>
                      <div className="absolute inset-0 bg-gradient-to-t from-black/0 via-transparent to-transparent" />
                    </div>
                  </motion.div>
                </>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Trust Section */}
      <section id="stats" className="py-20 border-y border-white/5 bg-zinc-900/50">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-12">
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
            <div className="text-3xl font-bold mb-1">5G</div>
            <div className={`text-sm ${mutedTextClass}`}>{t.stats.speed}</div>
          </div>
          <div className="flex flex-col items-center text-center">
            <div className={`mb-4 p-3 rounded-2xl border ${isDark ? 'bg-zinc-900 border-white/10' : 'bg-white border-zinc-200 shadow-sm'}`}>
              <ShieldCheck className={`w-6 h-6 ${mutedTextClass}`} />
            </div>
            <div className="text-3xl font-bold mb-1">AES-256</div>
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

      {/* Marquee Section - Forced LTR to maintain animation direction */}
      <div className="py-12 overflow-hidden bg-zinc-900 border-y border-white/5" dir="ltr">
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
               animation: scroll 240s linear infinite;
               width: max-content;
            }
            .animate-scroll:hover {
               animation-play-state: paused;
            }
         `}</style>
      </div>

      {/* App Showcase Section */}
      <section id="app" className="py-24 max-w-7xl mx-auto px-6 overflow-hidden">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            className="relative"
          >
            <div className={`absolute -inset-20 bg-blue-500/10 blur-[120px] rounded-full -z-10 transition-opacity duration-1000 ${mode === 'personal' ? 'opacity-100' : 'opacity-0'}`} />
            <div className={`absolute -inset-20 bg-purple-500/10 blur-[120px] rounded-full -z-10 transition-opacity duration-1000 ${mode === 'business' ? 'opacity-100' : 'opacity-0'}`} />

            <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">
              {t.hero.app_title}
            </h2>
            <p className={`text-xl ${mutedTextClass} mb-10 leading-relaxed`}>
              {t.hero.app_desc}
            </p>

            <div className="flex flex-wrap gap-4 mb-12">
              <Button size="lg" className="h-14 px-8 bg-zinc-900 border border-white/10 hover:bg-zinc-800 rounded-2xl text-white gap-3 transition-transform active:scale-95">
                <Download className="w-6 h-6" />
                <div className="text-left">
                  <div className="text-[10px] uppercase font-bold opacity-50">Download on the</div>
                  <div className="text-sm font-bold">{t.hero.app_ios}</div>
                </div>
              </Button>
              <Button size="lg" className="h-14 px-8 bg-zinc-900 border border-white/10 hover:bg-zinc-800 rounded-2xl text-white gap-3 transition-transform active:scale-95">
                <Smartphone className="w-6 h-6" />
                <div className="text-left">
                  <div className="text-[10px] uppercase font-bold opacity-50">Get it on</div>
                  <div className="text-sm font-bold">{t.hero.app_android}</div>
                </div>
              </Button>
            </div>

            <div className="grid grid-cols-2 gap-6">
              {[Zap, ShieldCheck, Database, Smartphone].map((Icon, i) => (
                <div key={i} className="flex gap-4 items-start">
                  <div className={`p-2 rounded-xl border ${cardBgClass} shrink-0`}>
                    <Icon className={`w-5 h-5 ${mode === 'personal' ? 'text-blue-500' : 'text-purple-500'}`} />
                  </div>
                  <div className="text-start">
                    <div className="font-bold text-sm mb-1 leading-tight">{t.hero.app_features[i]?.title}</div>
                    <div className="text-xs opacity-50 leading-tight">{t.hero.app_features[i]?.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50, rotateY: -20 }}
            whileInView={{ opacity: 1, x: 0, rotateY: 0 }}
            className="relative flex justify-center perspective-[1000px]"
          >
            <div className="relative w-full max-w-[400px]">
              <Image
                src="https://images.unsplash.com/photo-1616348436168-de43ad0db179?auto=format&fit=crop&q=80&w=800&h=1200"
                alt="App Interface"
                width={400}
                height={800}
                className="rounded-[3rem] border-8 border-zinc-900 shadow-2xl relative z-10"
              />
              <div className="absolute -bottom-10 -right-10 w-64 h-64 bg-blue-500/20 blur-3xl -z-10" />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Pricing / Packages */}
      <section id="pricing" className="py-24 max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">
            {mode === 'personal' ? t.pricing.b2c_title : t.pricing.b2b_title}
          </h2>
          <p className={`text-lg ${mutedTextClass} max-w-2xl mx-auto`}>
            {mode === 'personal' ? t.pricing.b2c_subtitle : t.pricing.b2b_subtitle}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {(mode === 'personal'
            ? [
              { id: 'light', price: '$9', features: [t.pricing.units.instant, t.pricing.units.hidden_fees], color: 'blue' },
              { id: 'nomad', price: '$29', features: [t.pricing.units.instant, t.pricing.units.hotspot, 'Full Speed'], highlight: true, color: 'blue' },
              { id: 'ultra', price: '$59', features: [t.pricing.units.instant, t.pricing.units.hotspot, 'Priority Support', 'Unlimited Term'], color: 'blue' }
            ]
            : [
              { id: 'startup', price: '$199', features: [t.pricing.units.api_access, '1 TB Shared Pool', t.pricing.units.pool_ip], color: 'purple' },
              { id: 'agency', price: '$899', features: [t.pricing.units.api_access, '5 TB Shared Pool', 'White Label Dashboard'], highlight: true, color: 'purple' },
              { id: 'platform', price: 'Custom', features: [t.pricing.units.api_access, 'Unlimited Pool', 'Custom Infrastructure'], color: 'purple' }
            ]
          ).map((p) => {
            const plan: Plan = {
              name: t.pricing.plans[p.id].name,
              price: p.price,
              desc: t.pricing.plans[p.id].desc,
              features: p.features
            }
            return (
              <motion.div
                key={p.id}
                whileHover={{ y: -8 }}
                className={`p-8 rounded-[32px] border ${p.highlight ? (p.color === 'blue' ? 'border-blue-500/50 bg-blue-500/5 ring-1 ring-blue-500/20' : 'border-purple-500/50 bg-purple-500/5 ring-1 ring-purple-500/20') : cardBgClass} relative overflow-hidden flex flex-col`}
              >
                {p.highlight && (
                  <div className={`absolute top-0 right-0 px-4 py-1 rounded-bl-2xl text-[10px] font-black uppercase tracking-widest ${p.color === 'blue' ? 'bg-blue-600 text-white' : 'bg-purple-600 text-white'}`}>
                    Most Popular
                  </div>
                )}
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-black">{plan.price}</span>
                    <span className={`text-sm ${mutedTextClass}`}>/{mode === 'personal' ? t.pricing.units.pack : t.pricing.units.month}</span>
                  </div>
                </div>
                <p className={`text-sm ${mutedTextClass} mb-8 flex-grow`}>
                  {plan.desc}
                </p>
                <div className="space-y-4 mb-8">
                  {plan.features.map((f, i) => (
                    <div key={i} className="flex items-center gap-3 text-sm">
                      <div className={`w-5 h-5 rounded-full ${p.color === 'blue' ? 'bg-blue-500/10' : 'bg-purple-500/10'} flex items-center justify-center`}>
                        <CheckCircle className={`w-3 h-3 ${p.color === 'blue' ? 'text-blue-500' : 'text-purple-500'}`} />
                      </div>
                      <span className="opacity-70">{f}</span>
                    </div>
                  ))}
                </div>
                <Button
                  onClick={() => handleSelectPlan(plan)}
                  className={`w-full h-12 rounded-2xl font-bold transition-all shadow-lg ${isDark ? 'bg-white text-black hover:bg-zinc-200' : 'bg-black text-white hover:bg-zinc-800'}`}
                >
                  {t.pricing.units.select}
                </Button>
              </motion.div>
            )
          })}
        </div>

        {/* B2B ROI Calculator inside Pricing */}
        {mode === 'business' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            className={`mt-16 p-10 rounded-[40px] border ${cardBgClass} bg-gradient-to-br from-purple-500/5 to-transparent text-center`}
          >
            <div className="max-w-xl mx-auto">
              <h3 className="text-2xl font-bold mb-6">{t.calculator.title}</h3>
              <div className="space-y-8">
                <div>
                  <div className="flex justify-between mb-4 text-sm font-bold opacity-70">
                    <span>{t.calculator.label}</span>
                    <span className="text-purple-500">{dataVal} TB</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="1000"
                    value={dataVal}
                    onChange={(e) => setDataVal(parseInt(e.target.value))}
                    className="w-full h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-purple-500"
                  />
                </div>
                <div className="p-6 rounded-3xl bg-white/5 border border-white/5">
                  <div className={`text-sm ${mutedTextClass} mb-2`}>{t.calculator.saving}</div>
                  <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-300">
                    ${(dataVal * 450).toLocaleString()}
                  </div>
                  <div className={`text-xs ${mutedTextClass} mt-1 uppercase tracking-widest font-bold`}>{t.calculator.per_year}</div>
                </div>
                <Button className="w-full h-14 rounded-2xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-lg">
                  {t.pricing.units.start}
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Global Startup / Innovation Section */}
        <section className="mt-32">
          <div className={`p-12 rounded-[48px] border ${cardBgClass} text-start relative overflow-hidden group`}>
            <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 blur-[100px] -z-10 group-hover:scale-110 transition-transform duration-1000" />
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-3xl font-bold mb-4">{t.startup_section.title}</h3>
                <p className={`text-lg ${mutedTextClass} mb-8`}>
                  {t.startup_section.desc}
                </p>
                <div className="flex flex-wrap gap-4">
                  {t.startup_section.features.map((f, i) => (
                    <div key={i} className="px-4 py-2 rounded-xl bg-white/5 border border-white/5 text-xs font-bold uppercase tracking-wider">
                      {f}
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex justify-center md:justify-end gap-4">
                <div className="w-24 h-24 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-center backdrop-blur-md">
                  <User className="w-8 h-8 opacity-20" />
                </div>
                <div className="w-24 h-24 mt-8 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-center backdrop-blur-md">
                  <Settings className="w-8 h-8 opacity-20" />
                </div>
                <div className="w-24 h-24 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-center backdrop-blur-md">
                  <ShieldCheck className="w-8 h-8 opacity-20" />
                </div>
              </div>
            </div>
          </div>
        </section>
      </section>

      {/* Testimonials */}
      <section className="py-24 max-w-7xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-center mb-16">{t.testimonials.title}</h2>
        <div className="grid md:grid-cols-2 gap-8">
          {t.testimonials.items.map((item: { name: string; role: string; text: string }, i: number) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`p-8 rounded-[32px] border ${cardBgClass} relative group`}
            >
              <Quote className="absolute top-8 right-8 w-12 h-12 text-blue-500/10 group-hover:text-blue-500/20 transition-colors" />
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500" />
                <div>
                  <div className="font-bold">{item.name}</div>
                  <div className={`text-xs ${mutedTextClass}`}>{item.role}</div>
                </div>
              </div>
              <p className="italic text-lg opacity-80 leading-relaxed">
                &ldquo;{item.text}&rdquo;
              </p>
              <div className="mt-6 flex gap-1">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 text-yellow-500 fill-yellow-500" />)}
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      <footer className="py-12 border-t border-white/5 text-center">
        <p className={`text-xs ${navTextClass}`}>
          {t.footer}
        </p>
      </footer>

      {/* Plan Configuration Overlay */}
      <AnimatePresence>
        {checkoutStep && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-md p-6"
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              className={`w-full max-w-lg rounded-[40px] border border-white/10 ${bgClass} shadow-2xl overflow-hidden relative`}
            >
              <button
                onClick={() => setCheckoutStep(null)}
                className="absolute top-6 right-6 w-10 h-10 rounded-full border border-white/5 flex items-center justify-center hover:bg-white/10 transition-colors z-10"
              >
                &times;
              </button>

              <div className="p-10">
                {checkoutStep === "config" && (
                  <div className="space-y-8">
                    <div className="text-center">
                      <div className="w-16 h-16 rounded-3xl bg-blue-500/10 flex items-center justify-center mx-auto mb-4">
                        <Settings className="w-8 h-8 text-blue-500" />
                      </div>
                      <h3 className="text-3xl font-black mb-1">{t.config.title}</h3>
                      <p className={`text-sm ${mutedTextClass}`}>{activePlan?.name} Base</p>
                    </div>

                    <div className="space-y-10">
                      {/* Data Slider */}
                      <div className="space-y-6">
                        <div className="flex justify-between items-end">
                          <div className="flex flex-col gap-1">
                            <span className="text-xs font-black uppercase tracking-widest opacity-40">{t.config.gb}</span>
                            <span className="text-4xl font-black">{customGB}</span>
                          </div>
                          <span className="text-blue-500 font-bold text-sm">GB</span>
                        </div>
                        <input
                          type="range"
                          min="1"
                          max="100"
                          value={customGB}
                          onChange={(e) => setCustomGB(parseInt(e.target.value))}
                          className="w-full h-3 bg-zinc-800 rounded-full appearance-none cursor-pointer accent-blue-500 hover:accent-blue-400 transition-all"
                        />

                        {/* Usage Visualization */}
                        <div className="grid grid-cols-3 gap-3">
                          <div className="p-4 rounded-3xl bg-white/5 border border-white/5 text-center">
                            <div className="text-xl font-black mb-0.5">~{Math.floor(customGB * 1.5)}</div>
                            <div className="text-[9px] uppercase font-bold opacity-40 leading-tight">{t.config.usage_video}</div>
                          </div>
                          <div className="p-4 rounded-3xl bg-white/5 border border-white/5 text-center">
                            <div className="text-xl font-black mb-0.5">~{customGB * 12}</div>
                            <div className="text-[9px] uppercase font-bold opacity-40 leading-tight">{t.config.usage_music}</div>
                          </div>
                          <div className="p-4 rounded-3xl bg-white/5 border border-white/5 text-center">
                            <div className="text-xl font-black mb-0.5">~{customGB * 15}</div>
                            <div className="text-[9px] uppercase font-bold opacity-40 leading-tight">{t.config.usage_social}</div>
                          </div>
                        </div>
                      </div>

                      {/* Mins Slider */}
                      <div className="space-y-6">
                        <div className="flex justify-between items-end">
                          <div className="flex flex-col gap-1">
                            <span className="text-xs font-black uppercase tracking-widest opacity-40">{t.config.mins}</span>
                            <span className="text-4xl font-black">{customMins}</span>
                          </div>
                          <span className="text-blue-500 font-bold text-sm">MIN</span>
                        </div>
                        <input
                          type="range"
                          min="0"
                          max="2000"
                          step="50"
                          value={customMins}
                          onChange={(e) => setCustomMins(parseInt(e.target.value))}
                          className="w-full h-3 bg-zinc-800 rounded-full appearance-none cursor-pointer accent-blue-500 hover:accent-blue-400 transition-all"
                        />
                      </div>

                      {/* SMS Toggle */}
                      <div className="flex items-center justify-between p-6 rounded-[32px] bg-white/5 border border-white/5 group hover:bg-white/10 transition-colors">
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 rounded-xl bg-yellow-500/10 flex items-center justify-center">
                            <Zap className="w-5 h-5 text-yellow-500" />
                          </div>
                          <span className="font-bold">{t.config.sms}</span>
                        </div>
                        <Switch checked={hasSMS} onCheckedChange={setHasSMS} />
                      </div>
                    </div>

                    <div className="pt-8 border-t border-white/5">
                      <div className="flex justify-between items-center mb-8">
                        <span className="text-xl opacity-50 font-bold">{t.config.total}</span>
                        <div className="text-right">
                          <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
                            ${calculateTotal().toFixed(2)}
                          </div>
                        </div>
                      </div>
                      <Button
                        size="lg"
                        className="w-full h-16 rounded-[24px] bg-blue-600 hover:bg-blue-500 text-white font-black text-xl shadow-[0_20px_50px_rgba(37,99,235,0.4)] transition-transform active:scale-95"
                        onClick={() => setCheckoutStep("payment")}
                      >
                        {t.config.confirm}
                      </Button>
                    </div>
                  </div>
                )}

                {checkoutStep === "payment" && (
                  <div className="space-y-8">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 rounded-2xl bg-purple-500/10 flex items-center justify-center">
                        <CreditCard className="w-6 h-6 text-purple-500" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold">{t.checkout.title}</h3>
                        <p className="text-sm opacity-50 uppercase tracking-widest font-bold">{t.checkout.step_final}</p>
                      </div>
                    </div>

                    <div className="p-6 rounded-3xl bg-zinc-900 border border-white/5 space-y-4 text-white">
                      <div className="flex justify-between text-sm">
                        <span className="opacity-50">{t.checkout.plan}</span>
                        <span className="font-bold">{activePlan?.name}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="opacity-50">{t.checkout.config}</span>
                        <span className="font-bold">{customGB}GB / {customMins}MIN</span>
                      </div>
                      <div className="h-px bg-white/5" />
                      <div className="flex justify-between font-black text-xl">
                        <span>{t.checkout.total_due}</span>
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
                          ${calculateTotal().toFixed(2)}
                        </span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <Button className="w-full h-14 rounded-2xl bg-white text-black hover:bg-zinc-200 font-bold transition-transform active:scale-95">
                        {t.checkout.apple_pay}
                      </Button>
                      <Button
                        className="w-full h-14 rounded-2xl bg-blue-600 text-white hover:bg-blue-500 font-bold"
                        onClick={() => setCheckoutStep("success")}
                      >
                        {t.checkout.pay_now}
                      </Button>
                    </div>
                  </div>
                )}

                {checkoutStep === "success" && (
                  <div className="text-center py-10 space-y-6">
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="w-20 h-20 bg-green-500/10 border border-green-500/30 rounded-full flex items-center justify-center mx-auto"
                    >
                      <CheckCircle className="w-10 h-10 text-green-500" />
                    </motion.div>
                    <div>
                      <h3 className="text-3xl font-bold mb-2">{t.checkout.success}</h3>
                      <p className={`text-sm ${mutedTextClass}`}>{t.checkout.success_desc}</p>
                    </div>
                    <Button
                      variant="outline"
                      className={`h-12 px-8 rounded-full ${isDark ? 'border-white/10 text-white' : 'border-zinc-200 text-black'}`}
                      onClick={() => setCheckoutStep(null)}
                    >
                      {t.checkout.close}
                    </Button>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Support Button */}
      <motion.a
        href="https://wa.me/message/CONNECT_GLOBAL" // Updated placeholder
        target="_blank"
        rel="noopener noreferrer"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className={`fixed bottom-8 ${lang === 'he' ? 'left-8' : 'right-8'} z-[60] w-14 h-14 bg-green-500 rounded-full flex items-center justify-center shadow-2xl text-white hover:bg-green-400 transition-colors`}
      >
        <Phone className="w-6 h-6" />
      </motion.a>
    </div>
  )
}
