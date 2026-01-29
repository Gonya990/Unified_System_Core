"use client"

import { useEffect, useState } from "react"
import { SkyBackground } from "./sky-background"
import { DestinationSelector } from "./destination-selector"

interface HeroSectionProps {
  isDark: boolean
}

export function HeroSection({ isDark }: HeroSectionProps) {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    // Trigger descend animation after mount
    const timer = setTimeout(() => setIsLoaded(true), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <SkyBackground variant={isDark ? "storm" : "day"} className="min-h-screen">
      <div className="flex flex-col items-center justify-center min-h-screen px-6">
        {/* Main heading with descend animation */}
        <div
          className={`text-center transition-all duration-1000 ${
            isLoaded ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-10"
          }`}
          style={{ transitionDelay: "200ms" }}
        >
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold text-white drop-shadow-lg mb-4 tracking-tight text-balance">
            We connect you
          </h1>
          <p className="text-xl md:text-2xl text-white/90 drop-shadow-md max-w-2xl mx-auto mb-12 text-pretty">
            Bridging distances, building relationships
          </p>
        </div>

        {/* Destination selector with descend animation */}
        <div
          className={`w-full max-w-md transition-all duration-1000 ${
            isLoaded ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-10"
          }`}
          style={{ transitionDelay: "500ms" }}
        >
          <DestinationSelector />
        </div>
      </div>
    </SkyBackground>
  )
}
