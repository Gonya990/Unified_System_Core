"use client"

import { Moon, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ThemeToggleProps {
  isDark: boolean
  setIsDark: (value: boolean) => void
}

export function ThemeToggle({ isDark, setIsDark }: ThemeToggleProps) {
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setIsDark(!isDark)}
      className="fixed top-6 right-6 z-50 rounded-full bg-card/80 backdrop-blur-sm border-border/50 hover:bg-accent transition-all duration-500"
    >
      {isDark ? (
        <Sun className="h-5 w-5 text-foreground transition-transform duration-500 rotate-0" />
      ) : (
        <Moon className="h-5 w-5 text-foreground transition-transform duration-500 rotate-0" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
