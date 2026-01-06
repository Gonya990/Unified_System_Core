"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { Globe, Wifi, Building2, Smartphone, ArrowRight, ShieldCheck, Zap, BarChart3, Database, Sun, Moon, Languages, Quote, Phone } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { motion, AnimatePresence } from "framer-motion"

import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { ALL_LANGUAGES } from "@/app/data/languages"
import { TRAVEL_PHOTOS, OFFICE_PHOTOS } from "@/app/data/photos"
import { translations } from "@/app/data/translations"



export default function ConnectivityHub() {
  const [mode, setMode] = useState<"personal" | "business">("personal")
  const [lang, setLang] = useState("ru")
  const [langOpen, setLangOpen] = useState(false)
  const [theme, setTheme] = useState<"dark" | "light">("dark")
  const [isDetected, setIsDetected] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setIsDetected(true), 2500)
    return () => clearTimeout(timer)
  }, [])

  const t = translations[lang as keyof typeof translations] || translations['en'] // Fallback to EN if translation missing

  // Theme logic
  const isDark = theme === 'dark'
  const bgClass = isDark ? "bg-black" : "bg-zinc-50"
  const textClass = isDark ? "text-white" : "text-zinc-900"
  const navBgClass = isDark ? "bg-black/50 border-white/5" : "bg-white/70 border-zinc-200"
  const cardBgClass = isDark ? "bg-zinc-900/50 border-white/5" : "bg-white border-zinc-200 shadow-lg"
  const mutedTextClass = isDark ? "text-zinc-400" : "text-zinc-500"
  const navTextClass = isDark ? "text-zinc-400 hover:text-white" : "text-zinc-600 hover:text-zinc-900"
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
                          value={language.label}
                          onSelect={() => {
                            setLang(language.value)
                            setLangOpen(false)
                          }}
                        >
                          {language.label}
                          <Check
                            className={cn(
                              "ms-auto h-4 w-4",
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
                      <ArrowRight className="ms-2 w-5 h-5" />
                    </Button>
                    <Button size="lg" variant="outline" className={`h-14 px-8 rounded-full text-lg ${isDark ? 'border-white/10 hover:bg-white/5 text-white' : 'border-zinc-200 hover:bg-zinc-100 text-black'}`}>
                      {t.hero.b2c_btn_2}
                    </Button>
                    <div className="mt-8 flex flex-col items-center">
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

                  {/* B2B Dashboard Mockup */}
                  <div className="mb-12 relative max-w-3xl mx-auto">
                    <div className={`absolute -inset-4 rounded-[40px] blur-3xl opacity-20 bg-purple-600`} />
                    <div className={`relative p-6 rounded-3xl border ${cardBgClass} backdrop-blur-xl overflow-hidden`}>
                      <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                          <span className="text-xs font-bold tracking-widest uppercase opacity-70">{t.dashboard.title}</span>
                        </div>
                        <div className="flex gap-2">
                          <div className="w-8 h-1 rounded-full bg-zinc-800" />
                          <div className="w-8 h-1 rounded-full bg-purple-500" />
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-6 mb-8 text-start">
                        <div>
                          <p className={`text-[10px] font-bold uppercase tracking-wider ${mutedTextClass} mb-1`}>{t.dashboard.nodes}</p>
                          <p className="text-2xl font-bold">1,402</p>
                        </div>
                        <div>
                          <p className={`text-[10px] font-bold uppercase tracking-wider ${mutedTextClass} mb-1`}>{t.dashboard.traffic}</p>
                          <p className="text-2xl font-bold text-purple-500">42.8 GB/s</p>
                        </div>
                        <div>
                          <p className={`text-[10px] font-bold uppercase tracking-wider ${mutedTextClass} mb-1`}>{t.dashboard.latency}</p>
                          <p className="text-2xl font-bold">14ms</p>
                        </div>
                      </div>

                      <div className="h-24 w-full flex items-end gap-1">
                        {[40, 70, 45, 90, 65, 80, 50, 40, 95, 75, 60, 85, 45, 90, 70, 100].map((h, i) => (
                          <motion.div
                            key={i}
                            className="flex-1 bg-gradient-to-t from-purple-500 to-pink-400 rounded-t-sm"
                            initial={{ height: 0 }}
                            animate={{ height: `${h}%` }}
                            transition={{ delay: i * 0.05, duration: 1, repeat: Infinity, repeatType: "reverse" }}
                          />
                        ))}
                      </div>

                      <div className={`mt-4 py-2 border-t ${isDark ? 'border-white/5' : 'border-zinc-200'} flex justify-between items-center`}>
                        <div className="flex items-center gap-2">
                          <ShieldCheck className="w-3 h-3 text-green-500" />
                          <span className="text-[10px] font-medium opacity-50">{t.dashboard.israel_optimized}</span>
                        </div>
                        <div className="flex gap-4">
                          <span className="text-[10px] font-mono opacity-50">ILI-TEL-AVIV-1</span>
                          <span className="text-[10px] font-mono opacity-50">US-EAST-1</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Startup Section Mini-Banner */}
                  <div className={`mb-12 p-6 rounded-3xl border ${isDark ? 'bg-blue-500/5 border-blue-500/20' : 'bg-blue-50 border-blue-100'} flex flex-col md:flex-row items-center gap-6 text-start`}>
                    <div className="flex-1">
                      <h4 className="font-bold text-lg mb-2">{t.startup_section.title}</h4>
                      <p className={`text-sm ${mutedTextClass}`}>{t.startup_section.desc}</p>
                    </div>
                    <div className="flex flex-wrap gap-3 justify-center md:justify-end">
                      {t.startup_section.features.map((f: string, i: number) => (
                        <span key={i} className={`text-[10px] font-bold px-3 py-1 rounded-full ${isDark ? 'bg-zinc-800 text-blue-400' : 'bg-white text-blue-600 border border-blue-100 shadow-sm'}`}>
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <Button
                      size="lg"
                      className="h-14 px-8 bg-purple-600 hover:bg-purple-500 rounded-full text-lg text-white"
                      onClick={() => document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })}
                    >
                      {t.hero.b2b_btn_1}
                      <Database className="ms-2 w-5 h-5" />
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
            <div className={`text-[10px] font-bold uppercase tracking-widest ${mutedTextClass} mb-1`}>Local Peering</div>
            <div className={`text-xs ${mutedTextClass} flex gap-2 items-center opacity-70`}>
              <span>Partner</span> • <span>Cellcom</span> • <span>Pelephone</span>
            </div>
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
               animation: scroll 240s linear infinite;
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
                  <div className="absolute top-0 rtl:left-0 ltr:right-0 p-6 opacity-0 group-hover:opacity-100 transition-opacity">
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
                  <div className="absolute top-0 rtl:left-0 ltr:right-0 p-6 opacity-0 group-hover:opacity-100 transition-opacity">
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

        {/* B2B ROI Calculator Section */}
        {mode === 'business' && (
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="max-w-4xl mx-auto px-6 py-20"
          >
            <div className={`p-10 rounded-[40px] border ${cardBgClass} backdrop-blur-3xl text-center relative overflow-hidden`}>
              <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-64 bg-purple-500/10 blur-[100px]" />
              <h2 className="text-3xl font-bold mb-10">{t.calculator.title}</h2>

              <div className="mb-12 max-w-xl mx-auto">
                <div className="flex justify-between mb-4 text-sm font-bold uppercase tracking-widest opacity-70">
                  <span>{t.calculator.label}</span>
                  <span className="text-purple-500">{(window as any).dataVal || 500} GB</span>
                </div>
                <input
                  type="range"
                  min="100"
                  max="10000"
                  step="100"
                  defaultValue="500"
                  onChange={(e) => {
                    const val = parseInt(e.target.value);
                    const savingElem = document.getElementById('saving-val');
                    if (savingElem) savingElem.innerText = `$${(val * 2.5).toLocaleString()}`;
                    (window as any).dataVal = val;
                  }}
                  className="w-full h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
              </div>

              <div className="inline-block p-8 rounded-3xl bg-purple-500/5 border border-purple-500/20">
                <p className={`text-sm ${mutedTextClass} mb-2`}>{t.calculator.saving}</p>
                <p id="saving-val" className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-300">
                  $1,250
                </p>
                <p className="text-sm font-bold mt-2 opacity-70 uppercase tracking-widest">{t.calculator.per_year}</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Testimonials Section */}
        <section className="max-w-7xl mx-auto px-6 py-24 border-t border-white/5">
          <h2 className="text-3xl font-bold text-center mb-16">{t.testimonials.title}</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {t.testimonials.items.map((item: any, i: number) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: i % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                className={`p-8 rounded-3xl border ${cardBgClass} relative`}
              >
                <Quote className="absolute top-6 rtl:left-6 ltr:right-6 w-8 h-8 opacity-10" />
                <p className="text-lg italic mb-6 leading-relaxed opacity-90">&ldquo;{item.text}&rdquo;</p>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold text-white shadow-lg">
                    {item.name[0]}
                  </div>
                  <div>
                    <p className="font-bold">{item.name}</p>
                    <p className={`text-xs ${mutedTextClass}`}>{item.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </section>
      </section >

      {/* Floating Support Button */}
      <motion.a
        href="https://wa.me/972500000000"
        target="_blank"
        rel="noopener noreferrer"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        className="fixed bottom-8 rtl:left-8 ltr:right-8 z-[100] w-16 h-16 bg-green-500 rounded-full flex items-center justify-center shadow-2xl overflow-hidden group"
      >
        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
        <Phone className="w-8 h-8 text-white relative z-10" />
        <span className="absolute rtl:right-20 ltr:left-[-180px] bg-black text-white px-4 py-2 rounded-xl text-sm font-bold opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap shadow-xl">
          {t.hero.support_whatsapp}
        </span>
      </motion.a>

      <footer className={`py-8 text-center text-sm ${mutedTextClass}`}>
        {t.footer}
      </footer>
    </div >
  )
}
