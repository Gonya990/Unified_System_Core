"use client"

import type React from "react"
import { useEffect, useState } from "react"
import { AnimatedClouds } from "./animated-clouds"

interface SkyBackgroundProps {
  variant: "day" | "night" | "storm"
  children?: React.ReactNode
  className?: string
}

export function SkyBackground({ variant, children, className = "" }: SkyBackgroundProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const gradients = {
    day: "from-[#87CEEB] via-[#ADD8E6] to-[#B0E0E6]", // Light sky blue palette
    night: "from-[#0a1628] via-[#1a2744] to-[#0d1b2a]", // Calm night navy
    storm: "from-[#1a1f2e] via-[#2d3548] to-[#1f2937]", // Stormy dark
  }

  return (
    <div className={`relative overflow-hidden transition-all duration-1000 ${className}`}>
      {/* Sky gradient */}
      <div className={`absolute inset-0 bg-gradient-to-b ${gradients[variant]} transition-all duration-1000`} />

      {/* Stars for night */}
      {variant === "night" && mounted && (
        <div className="absolute inset-0">
          {Array.from({ length: 80 }).map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-white animate-pulse"
              style={{
                width: Math.random() * 2.5 + 0.5 + "px",
                height: Math.random() * 2.5 + 0.5 + "px",
                top: Math.random() * 100 + "%",
                left: Math.random() * 100 + "%",
                opacity: Math.random() * 0.8 + 0.2,
                animationDelay: Math.random() * 4 + "s",
                animationDuration: 2 + Math.random() * 3 + "s",
              }}
            />
          ))}
        </div>
      )}

      {/* Animated clouds - white for day, grey for storm */}
      {mounted && (
        <AnimatedClouds
          isDark={variant !== "day"}
          intensity={variant === "storm" ? "heavy" : variant === "night" ? "light" : "medium"}
        />
      )}

      {/* Lightning effect for storm */}
      {variant === "storm" && mounted && (
        <div
          className="absolute inset-0 bg-white/30 pointer-events-none"
          style={{
            animation: "lightning 10s infinite",
            animationDelay: Math.random() * 6 + "s",
          }}
        />
      )}

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </div>
  )
}
