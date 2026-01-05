"use client"

import { useEffect, useRef, useState } from "react"
import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { popularDestinations } from "@/lib/destinations"

export function DestinationListSection() {
  const sectionRef = useRef<HTMLDivElement>(null)
  const [visibleItems, setVisibleItems] = useState<number[]>([])
  const [searchQuery, setSearchQuery] = useState("")

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = Number(entry.target.getAttribute("data-index"))
            setVisibleItems((prev) => [...new Set([...prev, index])])
          }
        })
      },
      { threshold: 0.2 },
    )

    const items = sectionRef.current?.querySelectorAll("[data-index]")
    items?.forEach((item) => observer.observe(item))

    return () => observer.disconnect()
  }, [])

  const filteredDestinations = popularDestinations.filter(
    (dest) =>
      dest.country.toLowerCase().includes(searchQuery.toLowerCase()) ||
      dest.cities.some((city) => city.toLowerCase().includes(searchQuery.toLowerCase())),
  )

  return (
    <section
      ref={sectionRef}
      className="relative py-24 px-6 bg-gradient-to-b from-background to-sky-50/30 dark:to-background"
    >
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-6xl font-bold mb-6 text-foreground text-balance">Popular Destinations</h2>
          <p className="text-muted-foreground text-xl md:text-2xl mb-10 max-w-2xl mx-auto leading-relaxed">
            Choose your destination and start connecting
          </p>

          <div className="max-w-xl mx-auto relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search destinations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-12 h-14 text-lg rounded-2xl shadow-lg"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredDestinations.map((destination, index) => {
            const isVisible = visibleItems.includes(index)

            return (
              <div
                key={destination.country}
                data-index={index}
                className={`group p-8 rounded-3xl bg-white/90 dark:bg-white/5 backdrop-blur-md shadow-lg hover:shadow-2xl hover:shadow-primary/20 transition-all duration-500 hover:scale-[1.03] hover:-translate-y-1 ${
                  isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
                }`}
                style={{ transitionDelay: `${index * 50}ms` }}
              >
                <div className="flex items-center gap-4 mb-6">
                  <div className="text-5xl group-hover:scale-110 transition-transform duration-300">
                    {destination.flag}
                  </div>
                  <h3 className="text-2xl font-bold text-foreground group-hover:text-primary transition-colors">
                    {destination.country}
                  </h3>
                </div>
                <div className="flex flex-wrap gap-3">
                  {destination.cities.map((city) => (
                    <Button
                      key={city}
                      variant="outline"
                      size="sm"
                      className="text-sm font-medium px-4 py-2 bg-sky-50/50 dark:bg-white/5 border-sky-200 dark:border-white/10 hover:bg-primary hover:text-white hover:border-primary transition-all duration-300 rounded-xl"
                    >
                      {city}
                    </Button>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
