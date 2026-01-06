"use client"

import { useState, useEffect, useRef } from "react"
import Link from "next/link"
import Image from "next/image"

import {
  Globe, Wifi, Building2, Smartphone, ArrowRight, ShieldCheck, Zap,
  BarChart3, Database, Sun, Moon, Languages, Quote, Phone,
  CreditCard, CheckCircle, Download, User, Settings, Star,
  Check, ChevronsUpDown, Code, Copy
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

const CURRENCIES = [
  { code: 'USD', symbol: '$', rate: 1 },
  { code: 'EUR', symbol: '€', rate: 0.92 },
  { code: 'ILS', symbol: '₪', rate: 3.7 },
  { code: 'RUB', symbol: '₽', rate: 90 },
]

const CODE_SNIPPETS = {
  bash: `curl -X POST "https://api.connect.global/v1/plans/order" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d "country=IL&gb=10&duration=30"`,
  node: `const axios = require('axios');

await axios.post('https://api.connect.global/v1/plans/order', {
  country: 'IL',
  gb: 10,
  duration: 30
}, {
  headers: { 'Authorization': 'Bearer YOUR_API_KEY' }
});`,
  python: `import requests

resp = requests.post(
    "https://api.connect.global/v1/plans/order",
    json={"country": "IL", "gb": 10, "duration": 30},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
print(resp.json())`
};

interface ConnectivityHubProps {
  initialCountry?: string
}

export default function ConnectivityHub({ initialCountry }: ConnectivityHubProps = {}) {
  const [mode, setMode] = useState<"personal" | "business">("personal")
  const [lang, setLang] = useState("en")
  const [langOpen, setLangOpen] = useState(false)
  const [langMobileOpen, setLangMobileOpen] = useState(false)
  const [theme, setTheme] = useState<"dark" | "light">("dark")
  const [isDetected, setIsDetected] = useState(false)
  const [dataVal, setDataVal] = useState(500)
  const [selectedCountry, setSelectedCountry] = useState(initialCountry || "")
  const [countryOpen, setCountryOpen] = useState(false)

  // Plan Config & Checkout
  const [activePlan, setActivePlan] = useState<Plan | null>(null)
  const [checkoutStep, setCheckoutStep] = useState<"config" | "payment" | "success" | null>(null)
  const [customGB, setCustomGB] = useState(5)
  const [customMins, setCustomMins] = useState(100)
  const [hasSMS, setHasSMS] = useState(false)
  const [currency, setCurrency] = useState(CURRENCIES[0])
  const [currencyOpen, setCurrencyOpen] = useState(false)

  // Travel Wizard & Advanced Options
  const [wizardOpen, setWizardOpen] = useState(false)
  const [wizardStep, setWizardStep] = useState(1)
  const [wizardData, setWizardData] = useState({
    destination: initialCountry || "",
    duration: "",
    usage: ""
  })
  const [neverExpiring, setNeverExpiring] = useState(false)
  const [vpnEnabled, setVpnEnabled] = useState(false)
  const [devTab, setDevTab] = useState<"bash" | "node" | "python">("bash")
  const [devCopied, setDevCopied] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)

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
    const totalUSD = base + (extraGB * 2) + (extraMins * 0.05) + (hasSMS ? 5 : 0) + (neverExpiring ? 5 : 0) + (vpnEnabled ? 3 : 0)
    return totalUSD * currency.rate
  }

  const formatPrice = (val: number | string) => {
    const num = typeof val === 'string' ? parseFloat(val.replace('$', '')) : val
    if (isNaN(num)) return val
    return `${currency.symbol}${(num * currency.rate).toFixed(currency.code === 'RUB' ? 0 : 2)}`
  }

  const handleCopy = () => {
    if (typeof window !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(CODE_SNIPPETS[devTab])
      setDevCopied(true)
      setTimeout(() => setDevCopied(false), 2000)
    }
  }

  const [platform, setPlatform] = useState({ os: "unknown", browser: "unknown" })

  // Track if language was loaded from storage
  const langLoadedRef = useRef(false)

  // Load saved language from localStorage on mount (with requestAnimationFrame to avoid lint warning)
  useEffect(() => {
    if (!langLoadedRef.current) {
      langLoadedRef.current = true
      const savedLang = localStorage.getItem('connect_lang')
      if (savedLang && savedLang !== lang) {
        requestAnimationFrame(() => setLang(savedLang))
      }
    }
  }, [lang])

  // Save language to localStorage when it changes
  const handleSetLang = (newLang: string) => {
    setLang(newLang)
    localStorage.setItem('connect_lang', newLang)
  }

  useEffect(() => {
    const timer = setTimeout(() => setIsDetected(true), 2500)

    // Platform detection (Client-only)
    const ua = window.navigator.userAgent.toLowerCase()
    const detectedOS = ua.includes("win") ? "windows" :
      ua.includes("mac") ? "mac" :
        ua.includes("linux") ? "linux" :
          ua.includes("android") ? "android" :
            (ua.includes("iphone") || ua.includes("ipad")) ? "ios" : "unknown"

    const detectedBrowser = (ua.includes("chrome") && !ua.includes("edg") && !ua.includes("opr")) ? "chrome" :
      (ua.includes("safari") && !ua.includes("chrome")) ? "safari" :
        ua.includes("edg") ? "edge" :
          ua.includes("firefox") ? "firefox" :
            (ua.includes("opr") || ua.includes("opera")) ? "opera" : "unknown"

    Promise.resolve().then(() => {
      setPlatform({ os: detectedOS, browser: detectedBrowser })
    })
    return () => clearTimeout(timer)
  }, [])

  // Sync theme with document element for Portals (Radix UI)
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [theme])

  // Theme logic
  const isDark = theme === 'dark'
  const bgClass = isDark ? "bg-[#111418]" : "bg-[#f5f2e8]" // Deep Charcoal vs Warm Sand Beige
  const textClass = isDark ? "text-zinc-100" : "text-stone-900"
  const navBgClass = isDark ? "bg-[#111418]/80 border-white/5" : "bg-[#f5f2e8]/80 border-stone-200"
  const cardBgClass = isDark ? "bg-[#1a1f26] border-white/5 shadow-2xl" : "bg-white/70 border-stone-100 shadow-md"
  const mutedTextClass = isDark ? "text-zinc-400" : "text-stone-500"
  const navTextClass = isDark ? "text-zinc-400 hover:text-zinc-100" : "text-stone-600 hover:text-stone-900"
  const isRTL = lang === 'he' || lang === 'ar' || lang === 'fa'

  return (
    <div
      dir={isRTL ? "rtl" : "ltr"}
      className={`min-h-screen ${bgClass} ${textClass} ${isDark ? 'dark' : ''} selection:bg-blue-500/30 font-sans transition-all duration-500 antialiased`}
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
            <button
              onClick={() => document.getElementById('app-showcase')?.scrollIntoView({ behavior: 'smooth' })}
              className={`${navTextClass} transition-colors cursor-pointer`}
            >
              {t.nav.tech}
            </button>
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
                            handleSetLang(currentValue)
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
                            handleSetLang(currentValue)
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

            <Popover open={currencyOpen} onOpenChange={setCurrencyOpen}>
              <PopoverTrigger asChild>
                <Button variant="ghost" size="sm" className={`h-8 gap-1 ${navTextClass} font-bold`}>
                  {currency.symbol} {currency.code}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-[120px] p-0 overflow-hidden" align="end">
                <div className={cn("grid", isDark ? "bg-zinc-900" : "bg-white")}>
                  {CURRENCIES.map((cur) => (
                    <button
                      key={cur.code}
                      onClick={() => {
                        setCurrency(cur)
                        setCurrencyOpen(false)
                      }}
                      className={cn(
                        "flex items-center justify-between px-3 py-2 text-xs font-bold hover:bg-blue-500/10 transition-colors",
                        currency.code === cur.code ? "text-blue-500 bg-blue-500/5" : mutedTextClass
                      )}
                    >
                      <span>{cur.code}</span>
                      <span className="opacity-50">{cur.symbol}</span>
                    </button>
                  ))}
                </div>
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

            <span className={`text-xs font-bold tracking-wider ${mode === 'personal' ? 'text-blue-500' : (isDark ? 'text-zinc-400' : 'text-stone-500')}`}>B2C</span>
            <Switch
              checked={mode === "business"}
              onCheckedChange={(c) => setMode(c ? "business" : "personal")}
              className="data-[state=checked]:bg-purple-600 data-[state=unchecked]:bg-blue-600"
            />
            <span className={`text-xs font-bold tracking-wider ${mode === 'business' ? 'text-purple-500' : (isDark ? 'text-zinc-400' : 'text-stone-500')}`}>B2B</span>
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
                  <div className="flex flex-wrap items-center justify-center gap-2 mb-8">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-500 text-xs">
                      <Wifi className="w-3 h-3" />
                      <span>{t.hero.b2c_tag}</span>
                    </div>
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-500/10 border border-zinc-500/20 text-zinc-500 text-[10px] uppercase font-bold tracking-widest">
                      <Settings className="w-2.5 h-2.5" />
                      <span>{platform.os !== "unknown" ? `${platform.os} × ${platform.browser}` : "Cross-Platform"} optimized</span>
                    </div>
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

                      <Button
                        size="lg"
                        variant="outline"
                        onClick={() => document.getElementById('app-showcase')?.scrollIntoView({ behavior: 'smooth' })}
                        className={`h-14 px-8 rounded-full text-lg w-full sm:w-auto ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}
                      >
                        {t.hero.b2c_btn_2}
                      </Button>
                    </div>

                    {/* Popular Destinations Chips */}
                    <div className="flex flex-wrap justify-center gap-2 max-w-3xl">
                      <span className={`text-xs font-bold uppercase tracking-widest ${mutedTextClass} w-full mb-2`}>
                        {t.hero.popular_dest}
                      </span>
                      {TOP_COUNTRIES.slice(0, 10).map((c) => (
                        <Link
                          key={c.code}
                          href={`/countries/${c.slug}`}
                          className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-medium transition-all hover:scale-105 active:scale-95 ${isDark ? 'bg-zinc-900 border-white/5 hover:border-blue-500/50 hover:bg-blue-500/10' : 'bg-white border-zinc-200 hover:border-blue-500/50 hover:bg-blue-50/50'}`}
                        >

                          <span>{c.flag}</span>
                          <span>{c.name}</span>
                        </Link>
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
                            15GB / {formatPrice(29)}
                          </motion.span>
                        )}
                      </div>
                    </div>

                    {/* Travel Wizard CTA */}
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      onClick={() => setWizardOpen(true)}
                      className={`mt-12 p-1 rounded-full bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-blue-500/20 border border-white/10 inline-flex items-center gap-4 pr-6 pl-2 backdrop-blur-sm group cursor-pointer hover:border-blue-500/50 transition-colors shadow-2xl overflow-hidden relative`}
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-blue-500/10 animate-pulse" />
                      <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center relative z-10 group-hover:rotate-12 transition-transform shadow-lg">
                        <Star className="w-5 h-5 text-white fill-white" />
                      </div>
                      <div className="relative z-10 text-start">
                        <div className="text-xs font-black uppercase tracking-tighter opacity-50">{t.wizard.title}</div>
                        <div className="text-sm font-bold flex items-center gap-1 text-start">
                          {t.wizard.desc}
                          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </div>
                      </div>
                    </motion.div>
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
                      onClick={() => document.getElementById('developer-preview')?.scrollIntoView({ behavior: 'smooth' })}
                      className="h-14 px-8 bg-purple-600 hover:bg-purple-500 rounded-full text-lg text-white active:scale-95 transition-transform"
                    >
                      {t.hero.b2b_btn_1}
                      <ArrowRight className="ms-2 w-5 h-5" />
                    </Button>
                    <Button
                      size="lg"
                      variant="outline"
                      onClick={() => window.open('https://wa.me/message/CONNECT_GLOBAL', '_blank')}
                      className={`h-14 px-8 rounded-full text-lg active:scale-95 transition-transform ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}
                    >
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

                  {/* API Developer Preview Section */}
                  <motion.div
                    id="developer-preview"
                    initial={{ opacity: 0, y: 40 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    className="mt-12 text-start max-w-5xl mx-auto w-full"
                  >
                    <div className="flex items-center gap-3 mb-6">
                      <Code className="w-6 h-6 text-purple-500" />
                      <h3 className="text-xl font-bold">{t.developer.title}</h3>
                    </div>
                    <div className={`rounded-2xl border border-white/10 ${bgClass} overflow-hidden shadow-xl`}>
                      <div className="flex border-b border-white/5 bg-white/5 overflow-x-auto">
                        <button
                          onClick={() => setDevTab("bash")}
                          className={`px-6 py-4 text-xs font-bold border-r border-white/5 transition-colors whitespace-nowrap ${devTab === "bash" ? 'bg-white/5 text-purple-400' : 'opacity-40 hover:opacity-100'}`}
                        >
                          {t.developer.bash_tab}
                        </button>
                        <button
                          onClick={() => setDevTab("node")}
                          className={`px-6 py-4 text-xs font-bold border-r border-white/5 transition-colors whitespace-nowrap ${devTab === "node" ? 'bg-white/5 text-purple-400' : 'opacity-40 hover:opacity-100'}`}
                        >
                          {t.developer.js_tab}
                        </button>
                        <button
                          onClick={() => setDevTab("python")}
                          className={`px-6 py-4 text-xs font-bold border-r border-white/5 transition-colors whitespace-nowrap ${devTab === "python" ? 'bg-white/5 text-purple-400' : 'opacity-40 hover:opacity-100'}`}
                        >
                          Python
                        </button>
                        <div className="flex-grow" />
                        <button
                          onClick={handleCopy}
                          className="px-4 py-3 text-xs flex items-center gap-2 hover:bg-white/5 transition-colors group relative"
                        >
                          <Copy className={`w-3 h-3 transition-colors ${devCopied ? 'text-green-500' : 'group-hover:text-purple-400'}`} />
                          <span className={`${devCopied ? 'text-green-500' : 'opacity-40'}`}>
                            {devCopied ? t.developer.copied : t.developer.copy}
                          </span>
                        </button>
                      </div>
                      <div className="relative group">
                        <pre className="p-4 md:p-8 text-xs md:text-sm overflow-x-auto font-mono bg-zinc-950/50 custom-scrollbar min-h-[200px]">
                          <code className="block leading-relaxed whitespace-pre md:whitespace-nowrap" dir="ltr">
                            {devTab === "bash" && (
                              <>
                                <span className="text-purple-400">curl</span> -X POST <span className="text-green-400">&quot;https://api.connect.global/v1/plans/order&quot;</span> \<br />
                                &nbsp;&nbsp;-H <span className="text-green-400">&quot;Authorization: Bearer YOUR_API_KEY&quot;</span> \<br />
                                &nbsp;&nbsp;-d <span className="text-green-400">&quot;country=IL&gb=10&duration=30&quot;</span>
                              </>
                            )}
                            {devTab === "node" && (
                              <>
                                <span className="text-purple-400">const</span> axios = <span className="text-purple-400">require</span>(<span className="text-green-400">&apos;axios&apos;</span>);<br /><br />
                                <span className="text-purple-400">await</span> axios.post(<span className="text-green-400">&apos;https://api.connect.global/v1/plans/order&apos;</span>, &#123;<br />
                                &nbsp;&nbsp;country: <span className="text-green-400">&apos;IL&apos;</span>,<br />
                                &nbsp;&nbsp;gb: <span className="text-cyan-400">10</span>,<br />
                                &nbsp;&nbsp;duration: <span className="text-cyan-400">30</span><br />
                                &#125;, &#123;<br />
                                &nbsp;&nbsp;headers: &#123; <span className="text-green-400">&apos;Authorization&apos;</span>: <span className="text-green-400">&apos;Bearer YOUR_API_KEY&apos;</span> &#125;<br />
                                &#125;);
                              </>
                            )}
                            {devTab === "python" && (
                              <>
                                <span className="text-purple-400">import</span> requests<br /><br />
                                resp = requests.post(<br />
                                &nbsp;&nbsp;&nbsp;&nbsp;<span className="text-green-400">&quot;https://api.connect.global/v1/plans/order&quot;</span>,<br />
                                &nbsp;&nbsp;&nbsp;&nbsp;json=&#123;<span className="text-green-400">&quot;country&quot;</span>: <span className="text-green-400">&quot;IL&quot;</span>, <span className="text-green-400">&quot;gb&quot;</span>: <span className="text-cyan-400">10</span>, <span className="text-green-400">&quot;duration&quot;</span>: <span className="text-cyan-400">30</span>&#125;,<br />
                                &nbsp;&nbsp;&nbsp;&nbsp;headers=&#123;<span className="text-green-400">&quot;Authorization&quot;</span>: <span className="text-green-400">&quot;Bearer YOUR_API_KEY&quot;</span>&#125;<br />
                                )<br />
                                <span className="text-purple-400">print</span>(resp.json())
                              </>
                            )}
                          </code>
                        </pre>
                        <div className="absolute top-4 right-4 text-[10px] font-black uppercase tracking-widest opacity-20 pointer-events-none">{devTab}</div>
                      </div>
                    </div>
                    <p className={`mt-4 text-xs font-medium uppercase tracking-widest ${mutedTextClass} opacity-50`}>{t.developer.subtitle}</p>
                  </motion.div>
                </>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* Trust Section */}
      <section id="stats" className="py-24 border-y border-white/5 bg-transparent relative overflow-hidden backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 relative z-10">
          {[
            { tag: "190+", label: t.stats.countries, icon: Globe, img: TRAVEL_PHOTOS[0] },
            { tag: "5G", label: t.stats.speed, icon: Zap, img: TRAVEL_PHOTOS[1] },
            { tag: "AES-256", label: t.stats.privacy, icon: ShieldCheck, img: OFFICE_PHOTOS[0] },
            { tag: "99.9%", label: t.stats.uptime, icon: BarChart3, img: OFFICE_PHOTOS[1] }
          ].map((stat, i) => (
            <div key={i} className="group relative flex flex-col items-center text-center p-8 rounded-[32px] overflow-hidden transition-all hover:scale-105 active:scale-95">
              {/* Background Photo (Semi-transparent with floating animation) */}
              <motion.div
                className="absolute inset-0 z-0 opacity-[0.05] grayscale group-hover:opacity-20 group-hover:grayscale-0 transition-all duration-700"
                animate={{
                  scale: [1, 1.1, 1],
                  rotate: [0, 1, 0]
                }}
                transition={{
                  duration: 10 + i * 2,
                  repeat: Infinity,
                  ease: "linear"
                }}
              >
                <Image
                  src={stat.img}
                  alt="stat bg"
                  fill
                  className="object-cover"
                />
              </motion.div>
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/5 dark:to-white/5 z-0" />

              <div className={`relative z-10 mb-6 p-4 rounded-3xl border transition-colors ${isDark ? 'bg-zinc-900/50 border-white/10 group-hover:border-blue-500/50' : 'bg-white/50 border-stone-200 group-hover:border-blue-500/50 shadow-sm'}`}>
                <stat.icon className={`w-8 h-8 transition-colors ${isDark ? 'text-zinc-400 group-hover:text-blue-400' : 'text-stone-500 group-hover:text-blue-500'}`} />
              </div>
              <div className="relative z-10 text-4xl font-black mb-2 tracking-tighter">{stat.tag}</div>
              <div className={`relative z-10 text-xs uppercase font-black tracking-widest ${mutedTextClass}`}>{stat.label}</div>
            </div>
          ))}
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
      <section id="app-showcase" className="py-24 max-w-7xl mx-auto px-6 overflow-hidden">
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
              <Button size="lg" onClick={() => alert('Connect iOS App: Coming Soon')} className="h-14 px-8 bg-zinc-900 border border-white/10 hover:bg-zinc-800 rounded-2xl text-white gap-3 transition-transform active:scale-95">
                <Download className="w-6 h-6" />
                <div className="text-left">
                  <div className="text-[10px] uppercase font-bold opacity-50">Download on the</div>
                  <div className="text-sm font-bold">{t.hero.app_ios}</div>
                </div>
              </Button>
              <Button size="lg" onClick={() => alert('Connect Android App: Coming Soon')} className="h-14 px-8 bg-zinc-900 border border-white/10 hover:bg-zinc-800 rounded-2xl text-white gap-3 transition-transform active:scale-95">
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

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {(mode === 'personal'
            ? [
              { id: 'light', price: '$9', features: [t.pricing.units.instant, t.pricing.units.hidden_fees], color: 'blue' },
              { id: 'nomad', price: '$29', features: [t.pricing.units.instant, t.pricing.units.hotspot, t.pricing.units.full_speed], highlight: true, color: 'blue' },
              { id: 'ultra', price: '$59', features: [t.pricing.units.instant, t.pricing.units.hotspot, t.pricing.units.priority_support, t.pricing.units.unlimited_term], color: 'blue' }
            ]
            : [
              { id: 'startup', price: '$199', features: [t.pricing.units.api_access, '1 ' + t.pricing.units.pool_label, t.pricing.units.pool_ip], color: 'purple' },
              { id: 'agency', price: '$899', features: [t.pricing.units.api_access, '5 ' + t.pricing.units.pool_label, t.pricing.units.white_label], highlight: true, color: 'purple' },
              { id: 'platform', price: 'Custom', features: [t.pricing.units.api_access, t.pricing.units.shared_pool, t.pricing.units.custom_infra], color: 'purple' }
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
                    {t.pricing.units.most_popular}
                  </div>
                )}
                <div className="mb-6">
                  <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-black">{formatPrice(plan.price)}</span>
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
                    {currency.symbol}{(dataVal * 450 * currency.rate).toLocaleString(undefined, { maximumFractionDigits: 0 })}
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

      {/* Travel Wizard Modal */}
      <AnimatePresence>
        {wizardOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[110] flex items-center justify-center bg-black/90 backdrop-blur-xl p-6"
          >
            <motion.div
              initial={{ scale: 0.9, y: 40 }}
              animate={{ scale: 1, y: 0 }}
              className={`w-full max-w-md rounded-[40px] border border-white/10 ${bgClass} shadow-2xl p-10 relative overflow-hidden`}
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 blur-3xl -z-10" />
              <button
                onClick={() => setWizardOpen(false)}
                className="absolute top-6 right-6 w-10 h-10 rounded-full border border-white/5 flex items-center justify-center hover:bg-white/10 transition-colors z-10"
              >
                &times;
              </button>

              <div className="space-y-8">
                <div className="text-center">
                  <div className="w-16 h-16 rounded-3xl bg-blue-600/20 flex items-center justify-center mx-auto mb-4">
                    <Star className="w-8 h-8 text-blue-500" />
                  </div>
                  <h3 className="text-2xl font-black">{t.wizard.title}</h3>
                  <p className={`text-sm ${mutedTextClass}`}>{t.wizard.desc}</p>
                </div>

                <div className="space-y-6">
                  {wizardStep === 1 && (
                    <div className="space-y-4">
                      <label className="text-xs font-black uppercase tracking-widest opacity-40">{t.wizard.step_1}</label>
                      <input
                        placeholder={t.hero.search_placeholder}
                        value={wizardData.destination}
                        className="w-full h-14 bg-white/5 border border-white/10 rounded-2xl px-6 focus:border-blue-500/50 outline-none transition-colors"
                        onChange={(e) => setWizardData({ ...wizardData, destination: e.target.value })}
                      />
                      <div className="flex flex-wrap gap-2 pt-2">
                        {TOP_COUNTRIES.filter(c =>
                          c.name.toLowerCase().includes(wizardData.destination.toLowerCase()) ||
                          c.code.toLowerCase().includes(wizardData.destination.toLowerCase())
                        ).slice(0, 5).map(c => (
                          <button
                            key={c.code}
                            onClick={() => {
                              setWizardData({ ...wizardData, destination: c.name });
                              setWizardStep(2);
                            }}
                            className="px-4 py-2 rounded-full border border-white/5 bg-white/5 text-xs hover:border-blue-500/50 transition-colors active:scale-95"
                          >
                            {c.flag} {c.name}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {wizardStep === 2 && (
                    <div className="space-y-4">
                      <label className="text-xs font-black uppercase tracking-widest opacity-40">{t.wizard.step_2}</label>
                      <div className="grid grid-cols-2 gap-4">
                        {t.wizard.durations.map((d, i) => (
                          <button key={i} onClick={() => {
                            setWizardData({ ...wizardData, duration: d });
                            setWizardStep(3);
                          }} className="h-14 rounded-2xl border border-white/5 bg-white/5 flex items-center justify-center font-bold hover:border-blue-500/50 transition-colors active:scale-95">
                            {d}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {wizardStep === 3 && (
                    <div className="space-y-4">
                      <label className="text-xs font-black uppercase tracking-widest opacity-40">{t.wizard.step_3}</label>
                      <div className="space-y-3">
                        {t.wizard.usage_types.map((u, i) => (
                          <button key={i} onClick={() => {
                            setWizardOpen(false);
                            setWizardStep(1);
                            // Recommend Nomad plan as default Assistant plan
                            handleSelectPlan({
                              name: `${wizardData.destination} Nomad`,
                              price: '$29',
                              desc: t.wizard.result,
                              features: [t.pricing.units.instant, t.pricing.units.full_speed]
                            });
                          }} className="w-full h-14 rounded-2xl border border-white/5 bg-white/5 flex items-center justify-start px-6 font-bold hover:border-blue-500/50 transition-colors active:scale-95">
                            {u}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex justify-between items-center pt-8">
                  <div className="flex gap-2">
                    {[1, 2, 3].map(s => (
                      <div key={s} className={`w-2 h-2 rounded-full transition-all ${wizardStep === s ? 'w-6 bg-blue-500' : 'bg-white/10'}`} />
                    ))}
                  </div>
                  {wizardStep > 1 && (
                    <button onClick={() => setWizardStep(wizardStep - 1)} className="text-xs font-bold opacity-40 hover:opacity-100 uppercase tracking-widest transition-opacity flex items-center gap-1">
                      &larr; {t.wizard.back}
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

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
              className={`w-full max-w-[380px] max-h-[90vh] rounded-[40px] border border-white/10 ${bgClass} shadow-2xl overflow-hidden relative flex flex-col`}
            >
              <button
                onClick={() => setCheckoutStep(null)}
                className="absolute top-6 right-6 w-10 h-10 rounded-full border border-white/5 flex items-center justify-center hover:bg-white/10 transition-colors z-10"
              >
                &times;
              </button>

              <div className="p-8 overflow-y-auto custom-scrollbar">
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
                          className="w-full relative z-10"
                        />

                        {/* Usage Visualization with Logos */}
                        <div className="grid grid-cols-3 gap-3">
                          <div className="p-4 rounded-3xl bg-white/5 border border-white/5 flex flex-col items-center gap-2 group hover:bg-white/10 transition-colors">
                            <div className="flex gap-1.5 opacity-60 group-hover:opacity-100 transition-opacity">
                              <div className="w-5 h-5 bg-red-600 rounded-sm flex items-center justify-center text-[7px] font-black text-white">Y</div>
                              <div className="w-5 h-5 bg-black rounded-sm flex items-center justify-center text-[7px] font-black text-red-600 border border-red-600/20">N</div>
                            </div>
                            <div className="text-xl font-black">~{Math.floor(customGB * 1.5)}h</div>
                            <div className="text-[8px] uppercase font-bold opacity-30 leading-tight text-center">{t.config.usage_video}</div>
                          </div>
                          <div className="p-4 rounded-3xl bg-white/5 border border-white/5 flex flex-col items-center gap-2 group hover:bg-white/10 transition-colors">
                            <div className="flex gap-1.5 opacity-60 group-hover:opacity-100 transition-opacity">
                              <div className="w-5 h-5 bg-[#1DB954] rounded-full flex items-center justify-center text-[7px] font-black text-black">S</div>
                              <div className="w-5 h-5 bg-[#FC3C44] rounded-full flex items-center justify-center text-[7px] font-black text-white">A</div>
                            </div>
                            <div className="text-xl font-black">~{customGB * 12}h</div>
                            <div className="text-[8px] uppercase font-bold opacity-30 leading-tight text-center">{t.config.usage_music}</div>
                          </div>
                          <div className="p-4 rounded-3xl bg-white/5 border border-white/5 flex flex-col items-center gap-2 group hover:bg-white/10 transition-colors">
                            <div className="flex gap-1.5 opacity-60 group-hover:opacity-100 transition-opacity">
                              <div className="w-5 h-5 bg-gradient-to-tr from-[#f9ce34] via-[#ee2a7b] to-[#6228d7] rounded-md flex items-center justify-center text-[7px] font-black text-white">I</div>
                              <div className="w-5 h-5 bg-black rounded-md flex items-center justify-center text-[7px] font-black text-[#00f2ea]">T</div>
                            </div>
                            <div className="text-xl font-black">~{customGB * 15}h</div>
                            <div className="text-[8px] uppercase font-bold opacity-30 leading-tight text-center">{t.config.usage_social}</div>
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
                          className="w-full relative z-10"
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

                      {/* Advanced Toggles */}
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-6 rounded-[32px] bg-white/5 border border-white/5 group hover:bg-white/10 transition-colors">
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center">
                              <ShieldCheck className="w-5 h-5 text-blue-500" />
                            </div>
                            <div>
                              <div className="font-bold">Secure Tunnel (VPN)</div>
                              <div className="text-[10px] opacity-40 font-bold uppercase tracking-widest">+ $3 / pack</div>
                            </div>
                          </div>
                          <Switch checked={vpnEnabled} onCheckedChange={setVpnEnabled} />
                        </div>
                        <div className="flex items-center justify-between p-6 rounded-[32px] bg-white/5 border border-white/5 group hover:bg-white/10 transition-colors">
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
                              <Wifi className="w-5 h-5 text-purple-500" />
                            </div>
                            <div>
                              <div className="font-bold">Never Expire</div>
                              <div className="text-[10px] opacity-40 font-bold uppercase tracking-widest">+ $5 / pack</div>
                            </div>
                          </div>
                          <Switch checked={neverExpiring} onCheckedChange={setNeverExpiring} />
                        </div>
                      </div>
                    </div>

                    <div className="pt-8 border-t border-white/5">
                      <div className="flex justify-between items-center mb-8">
                        <span className="text-xl opacity-50 font-bold">{t.config.total}</span>
                        <div className="text-right">
                          <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
                            {formatPrice(calculateTotal())}
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
                          {formatPrice(calculateTotal())}
                        </span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <Button
                        disabled={isProcessing}
                        className="w-full h-14 rounded-2xl bg-white text-black hover:bg-zinc-200 font-bold transition-transform active:scale-95 flex items-center justify-center gap-2"
                        onClick={() => {
                          setIsProcessing(true);
                          setTimeout(() => {
                            setIsProcessing(false);
                            setCheckoutStep("success");
                          }, 1500);
                        }}
                      >
                        {isProcessing ? (
                          <div className="w-5 h-5 border-2 border-black/20 border-t-black rounded-full animate-spin" />
                        ) : (
                          platform.os === "mac" || platform.os === "ios" ? (
                            <><Download className="w-5 h-5" /> {t.checkout.apple_pay}</>
                          ) : (
                            <><CreditCard className="w-5 h-5" /> Google Pay / Card</>
                          )
                        )}
                      </Button>
                      <Button
                        disabled={isProcessing}
                        className="w-full h-14 rounded-2xl bg-blue-600 text-white hover:bg-blue-500 font-bold relative overflow-hidden group"
                        onClick={() => {
                          setIsProcessing(true);
                          setTimeout(() => {
                            setIsProcessing(false);
                            setCheckoutStep("success");
                          }, 1500);
                        }}
                      >
                        {isProcessing ? (
                          <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin mx-auto" />
                        ) : (
                          t.checkout.pay_now
                        )}
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
        className={`fixed bottom-8 ${lang === 'he' ? 'left-8' : 'right-8'} z-[60] w-14 h-14 bg-green-500 rounded-full flex items-center justify-center shadow-2xl text-white hover:bg-green-400 transition-colors cursor-pointer`}
      >
        <Phone className="w-6 h-6" />
      </motion.a>

      {/* Footer Section */}
      <footer className={`py-20 border-t border-white/5 ${bgClass} relative z-10`}>
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-12 mb-16">
            <div className="col-span-2 lg:col-span-2">
              <div className="flex items-center gap-2 mb-6">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-black text-white italic">C</div>
                <span className="text-xl font-bold tracking-tighter text-white">CONNECT.GLOBAL</span>
              </div>
              <p className={`text-sm ${mutedTextClass} max-w-xs mb-8`}>
                Next-generation eSIM infrastructure for global travelers and enterprises.
                Reliable connectivity in 190+ countries.
              </p>
              <div className="flex gap-4">
                {['Twitter', 'Instagram', 'LinkedIn'].map(s => (
                  <button key={s} onClick={() => alert(`${s} page: Coming Soon`)} className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 transition-colors group">
                    <Star className="w-4 h-4 opacity-50 group-hover:text-blue-500 transition-colors" />
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-bold mb-6 text-sm uppercase tracking-widest text-white">{t.nav.coverage}</h4>
              <ul className="space-y-4 text-sm opacity-50 font-medium">
                <li><button onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-blue-500 transition-colors">Europe</button></li>
                <li><button onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-blue-500 transition-colors">Asia</button></li>
                <li><button onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-blue-500 transition-colors">Middle East</button></li>
                <li><button onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-blue-500 transition-colors">Americas</button></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold mb-6 text-sm uppercase tracking-widest text-white">Solutions</h4>
              <ul className="space-y-4 text-sm opacity-50 font-medium">
                <li><button onClick={() => setMode('personal')} className="hover:text-blue-500 transition-colors">For Personal</button></li>
                <li><button onClick={() => setMode('business')} className="hover:text-purple-500 transition-colors">For Business</button></li>
                <li><button onClick={() => document.getElementById('developer-preview')?.scrollIntoView({ behavior: 'smooth' })} className="hover:text-purple-500 transition-colors">API Docs</button></li>
                <li><button onClick={() => window.open('https://wa.me/message/CONNECT_GLOBAL')} className="hover:text-green-500 transition-colors">Support</button></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold mb-6 text-sm uppercase tracking-widest text-white">Legal</h4>
              <ul className="space-y-4 text-sm opacity-50 font-medium">
                <li><button onClick={() => alert('Terms of Service: Coming Soon')} className="hover:text-blue-500 transition-colors">Terms of Service</button></li>
                <li><button onClick={() => alert('Privacy Policy: Coming Soon')} className="hover:text-blue-500 transition-colors">Privacy Policy</button></li>
                <li><button onClick={() => alert('Refund Policy: Coming Soon')} className="hover:text-blue-500 transition-colors">Refund Policy</button></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6 text-xs font-bold uppercase tracking-widest opacity-30">
            <div className="text-white">{t.footer}</div>
            <div className="flex gap-8 text-white">
              <span>Status: All Operational</span>
              <span>v1.2.0</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
