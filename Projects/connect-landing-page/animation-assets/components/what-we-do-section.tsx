"use client"

import { useEffect, useRef, useState } from "react"
import { Globe, Users, Building2 } from "lucide-react"

const services = [
  {
    icon: Users,
    title: "Personal Connections",
    stat: "10M+",
    description: "People connected worldwide",
  },
  {
    icon: Building2,
    title: "Business Networks",
    stat: "500K+",
    description: "Companies collaborating",
  },
  {
    icon: Globe,
    title: "Global Reach",
    stat: "190+",
    description: "Countries and regions",
  },
]

export function WhatWeDoSection() {
  const sectionRef = useRef<HTMLDivElement>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.2 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <section ref={sectionRef} className="py-20 px-6 bg-background">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <span className="text-primary font-medium tracking-wide uppercase text-sm">What We Do</span>
          <h2 className="text-4xl md:text-5xl font-bold mt-4 mb-6 text-foreground">
            Connecting the <span className="text-primary">entire world</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Our platform brings together individuals, families, and businesses from every corner of the globe. Through
            innovative technology and a passion for connection, we make the impossible possible.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {services.map((service, index) => {
            const Icon = service.icon
            return (
              <div
                key={service.title}
                className={`text-center p-8 rounded-xl bg-card border border-border hover:border-primary/50 transition-all duration-700 hover:shadow-lg ${
                  isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
                }`}
                style={{ transitionDelay: `${index * 150}ms` }}
              >
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6">
                  <Icon className="w-8 h-8 text-primary" />
                </div>
                <div className="text-4xl font-bold text-foreground mb-2">{service.stat}</div>
                <h3 className="text-xl font-semibold mb-2 text-foreground">{service.title}</h3>
                <p className="text-muted-foreground">{service.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
