"use client"

import { useEffect, useRef, useState } from "react"
import { Target, Lightbulb, Rocket } from "lucide-react"

const features = [
  {
    icon: Target,
    title: "Our Mission",
    description:
      "To create meaningful connections that transcend borders, cultures, and distances. We believe that every person deserves access to a global community.",
  },
  {
    icon: Lightbulb,
    title: "Our Vision",
    description:
      "A world where distance is no barrier to human connection. Where technology serves to bring us closer, not further apart.",
  },
  {
    icon: Rocket,
    title: "Our Solution",
    description:
      "Innovative technology that makes connecting simple, secure, and seamless. Built for people, powered by purpose.",
  },
]

export function AboutSection() {
  const sectionRef = useRef<HTMLDivElement>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.15 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <section className="py-32 px-6 bg-gradient-to-b from-sky-50/50 to-background dark:from-background dark:to-background">
      <div ref={sectionRef} className="max-w-6xl mx-auto">
        <div
          className={`text-center mb-16 transition-all duration-1000 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
          }`}
        >
          <span className="text-primary font-medium tracking-wide uppercase text-sm">Who We Are</span>
          <h2 className="text-4xl md:text-6xl font-bold mt-4 mb-6 text-foreground text-balance">
            Building bridges, <span className="text-primary">not walls</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
            {"We're on a mission to make the world feel smaller, one connection at a time."}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div
                key={feature.title}
                className={`p-8 rounded-2xl bg-card border border-border hover:border-primary/50 hover:bg-accent transition-all duration-700 hover:shadow-lg ${
                  isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
                }`}
                style={{ transitionDelay: `${300 + index * 200}ms` }}
              >
                <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-6">
                  <Icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-foreground">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
