"use client"

import React, { useEffect, useState, useMemo } from "react"
import { AnimatedClouds } from "./animated-clouds"

interface SkyBackgroundProps {
  variant: "day" | "night" | "storm"
  children?: React.ReactNode
  className?: string
}

interface Star {
  width: string
  height: string
  top: string
  left: string
  opacity: number
  delay: string
  duration: string
}

export function SkyBackground({ variant, children, className = "" }: SkyBackgroundProps) {
  const [mounted, setMounted] = useState(false)
  const [stars, setStars] = useState<Star[]>([])
  const [lightningDelay, setLightningDelay] = useState("0s")

  useEffect(() => {
    setMounted(true)

    // Generate star properties after mount to maintain purity during render
    const generatedStars = Array.from({ length: 80 }).map(() => ({
      width: (Math.random() * 2.5 + 0.5).toFixed(2) + "px",
      height: (Math.random() * 2.5 + 0.5).toFixed(2) + "px",
      top: (Math.random() * 100).toFixed(2) + "%",
      left: (Math.random() * 100).toFixed(2) + "%",
      opacity: Number((Math.random() * 0.8 + 0.2).toFixed(2)),
      delay: (Math.random() * 4).toFixed(2) + "s",
      duration: (2 + Math.random() * 3).toFixed(2) + "s",
    }))
    setStars(generatedStars)
    setLightningDelay((Math.random() * 6).toFixed(2) + "s")
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
          {stars.map((star, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-white animate-pulse"
              style={{
                width: star.width,
                height: star.height,
                top: star.top,
                left: star.left,
                opacity: star.opacity,
                animationDelay: star.delay,
                animationDuration: star.duration,
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
            animationDelay: lightningDelay,
          }}
        />
      )}

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </div>
  )
}
