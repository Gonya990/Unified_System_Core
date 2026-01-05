"use client"

import { useState, useEffect } from "react"
import { HeroSection } from "@/components/hero-section"
import { DestinationListSection } from "@/components/destination-list-section"
import { AboutSection } from "@/components/about-section"
import { WhatWeDoSection } from "@/components/what-we-do-section"
import { FAQSection } from "@/components/faq-section"
import { Footer } from "@/components/footer"
import { ThemeToggle } from "@/components/theme-toggle"
import { RainEffect } from "@/components/rain-effect"

export default function Home() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }, [isDark])

  return (
    <main className="relative min-h-screen overflow-x-hidden">
      <ThemeToggle isDark={isDark} setIsDark={setIsDark} />
      {isDark && <RainEffect />}
      <HeroSection isDark={isDark} />
      <DestinationListSection />
      <AboutSection />
      <WhatWeDoSection />
      <FAQSection />
      <Footer />
    </main>
  )
}
