"use client"

import { useState, useRef, useEffect } from "react"
import { MapPin, Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { popularDestinations } from "@/lib/destinations"

export function DestinationSelector() {
  const [destination, setDestination] = useState("")
  const [showDropdown, setShowDropdown] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const filteredDestinations = destination
    ? popularDestinations.filter(
        (dest) =>
          dest.country.toLowerCase().includes(destination.toLowerCase()) ||
          dest.cities.some((city) => city.toLowerCase().includes(destination.toLowerCase())),
      )
    : popularDestinations.slice(0, 6) // Show top 6 when empty

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  return (
    <div className="bg-white/95 dark:bg-slate-800/90 backdrop-blur-md rounded-2xl p-6 shadow-2xl shadow-black/10 border border-white/30 dark:border-white/10">
      <div className="flex flex-col gap-4">
        <div className="flex items-center gap-3 text-slate-700 dark:text-slate-200">
          <MapPin className="w-5 h-5 text-sky-500 dark:text-sky-400" />
          <span className="font-medium">Where do you want to connect?</span>
        </div>

        <div className="relative" ref={dropdownRef}>
          <Input
            type="text"
            placeholder="Enter destination..."
            value={destination}
            onChange={(e) => {
              setDestination(e.target.value)
              setShowDropdown(true)
            }}
            onFocus={() => setShowDropdown(true)}
            className="pl-4 pr-12 py-6 text-lg rounded-xl bg-slate-50 dark:bg-slate-700/50 border-slate-200 dark:border-slate-600 focus:border-sky-400 transition-colors text-slate-800 dark:text-white placeholder:text-slate-400"
          />
          <Button
            size="icon"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg bg-sky-500 hover:bg-sky-600 text-white"
          >
            <Search className="w-4 h-4" />
          </Button>

          {showDropdown && filteredDestinations.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-slate-800 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-600 max-h-96 overflow-y-auto z-50">
              {filteredDestinations.map((dest) => (
                <div key={dest.country} className="border-b border-slate-100 dark:border-slate-700 last:border-0">
                  <button
                    onClick={() => {
                      setDestination(dest.country)
                      setShowDropdown(false)
                    }}
                    className="w-full flex items-center gap-3 px-4 py-3 hover:bg-sky-50 dark:hover:bg-slate-700 transition-colors text-left"
                  >
                    <span className="text-2xl">{dest.flag}</span>
                    <span className="font-semibold text-slate-800 dark:text-white">{dest.country}</span>
                  </button>
                  <div className="flex flex-wrap gap-2 px-4 pb-3">
                    {dest.cities.map((city) => (
                      <button
                        key={city}
                        onClick={() => {
                          setDestination(city)
                          setShowDropdown(false)
                        }}
                        className="text-sm px-3 py-1 rounded-full bg-sky-50 dark:bg-slate-700 hover:bg-sky-100 dark:hover:bg-slate-600 text-sky-700 dark:text-sky-300 transition-colors"
                      >
                        {city}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="flex flex-wrap gap-2 pt-2">
          {["Nearby", "Global", "Virtual"].map((tag) => (
            <button
              key={tag}
              className="px-4 py-2 text-sm rounded-full bg-sky-50 dark:bg-slate-700 hover:bg-sky-100 dark:hover:bg-slate-600 text-sky-700 dark:text-sky-300 transition-colors font-medium"
            >
              {tag}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
