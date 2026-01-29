"use client"

import { useEffect, useRef } from "react"

export function RainEffect() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
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

    interface Raindrop {
      x: number
      y: number
      length: number
      speed: number
      opacity: number
    }

    const raindrops: Raindrop[] = Array.from({ length: 300 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      length: Math.random() * 25 + 15,
      speed: Math.random() * 18 + 12,
      opacity: Math.random() * 0.4 + 0.15,
    }))

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Rain color - light blue-grey
      ctx.strokeStyle = "rgba(180, 200, 220, 0.6)"
      ctx.lineWidth = 1.5

      raindrops.forEach((drop) => {
        ctx.beginPath()
        ctx.globalAlpha = drop.opacity
        ctx.moveTo(drop.x, drop.y)
        // Angled rain for wind effect
        ctx.lineTo(drop.x + 2, drop.y + drop.length)
        ctx.stroke()

        drop.y += drop.speed
        drop.x += 1.5 // Wind drift

        if (drop.y > canvas.height) {
          drop.y = -drop.length
          drop.x = Math.random() * canvas.width
        }
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener("resize", resizeCanvas)
      cancelAnimationFrame(animationRef.current)
    }
  }, [])

  return (
    <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-40" style={{ mixBlendMode: "screen" }} />
  )
}
