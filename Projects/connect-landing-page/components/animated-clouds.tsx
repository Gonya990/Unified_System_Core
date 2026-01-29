"use client"

import { useEffect, useRef } from "react"

interface Cloud {
  id: number
  x: number
  y: number
  scale: number
  speed: number
  opacity: number
  depth: number
}

interface AnimatedCloudsProps {
  isDark?: boolean
  intensity?: "light" | "medium" | "heavy"
}

export function AnimatedClouds({ isDark = false, intensity = "medium" }: AnimatedCloudsProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const cloudsRef = useRef<Cloud[]>([])
  const animationRef = useRef<number>(0)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener("resize", resizeCanvas)

    const cloudCount = intensity === "light" ? 6 : intensity === "medium" ? 10 : 16

    // Initialize clouds with varied positions
    cloudsRef.current = Array.from({ length: cloudCount }, (_, i) => ({
      id: i,
      x: Math.random() * canvas.width * 1.5 - canvas.width * 0.25,
      y: Math.random() * canvas.height * 0.6 + canvas.height * 0.05,
      scale: 0.6 + Math.random() * 1.2,
      speed: 0.15 + Math.random() * 0.4,
      opacity: 0.5 + Math.random() * 0.4,
      depth: Math.random(),
    }))

    const drawCloud = (cloud: Cloud) => {
      const baseColor = isDark ? [100, 105, 115] : [255, 255, 255]
      const shadowColor = isDark ? [60, 65, 75] : [190, 195, 205]

      ctx.save()
      ctx.translate(cloud.x, cloud.y)
      ctx.scale(cloud.scale, cloud.scale)
      ctx.globalAlpha = cloud.opacity * (1 - cloud.depth * 0.4)

      // Fluffy cloud shape with multiple overlapping circles
      const circles = [
        { x: 0, y: 0, r: 55 },
        { x: 45, y: -8, r: 45 },
        { x: -35, y: 5, r: 42 },
        { x: 22, y: 12, r: 38 },
        { x: -18, y: -12, r: 32 },
        { x: 55, y: 8, r: 32 },
        { x: -55, y: 8, r: 28 },
        { x: 30, y: -18, r: 25 },
      ]

      // Shadow layer for depth
      ctx.fillStyle = `rgba(${shadowColor.join(",")}, 0.35)`
      circles.forEach((c) => {
        ctx.beginPath()
        ctx.arc(c.x + 4, c.y + 6, c.r, 0, Math.PI * 2)
        ctx.fill()
      })

      // Main cloud body
      ctx.fillStyle = `rgba(${baseColor.join(",")}, ${isDark ? 0.75 : 0.95})`
      circles.forEach((c) => {
        ctx.beginPath()
        ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2)
        ctx.fill()
      })

      // Bright highlights for 3D effect
      if (!isDark) {
        ctx.fillStyle = `rgba(255, 255, 255, 0.5)`
        circles.slice(0, 4).forEach((c) => {
          ctx.beginPath()
          ctx.arc(c.x - 8, c.y - 12, c.r * 0.4, 0, Math.PI * 2)
          ctx.fill()
        })
      }

      ctx.restore()
    }

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Sort clouds by depth for proper layering
      const sortedClouds = [...cloudsRef.current].sort((a, b) => b.depth - a.depth)

      sortedClouds.forEach((cloud) => {
        cloud.x += cloud.speed * (0.6 + (1 - cloud.depth) * 0.4)
        // Gentle vertical float
        cloud.y += Math.sin(Date.now() * 0.0008 + cloud.id * 0.5) * 0.15

        // Reset cloud position when off screen
        if (cloud.x > canvas.width + 250) {
          cloud.x = -250
          cloud.y = Math.random() * canvas.height * 0.6 + canvas.height * 0.05
        }

        drawCloud(cloud)
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener("resize", resizeCanvas)
      cancelAnimationFrame(animationRef.current)
    }
  }, [isDark, intensity])

  return <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none" style={{ zIndex: 1 }} />
}
