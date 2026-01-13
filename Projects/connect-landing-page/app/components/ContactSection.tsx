"use client"

import { useState, useRef } from "react"
import type { FormEvent } from "react"
import { motion } from "framer-motion"
import { Mail, MapPin, Phone, Send } from "lucide-react"

import { Button } from "@/components/ui/button"
import { sendContactEmail } from "@/app/actions/contact"

type StatusState = {
  type: "success" | "error"
  message: string
}

export default function ContactSection() {
  const [status, setStatus] = useState<StatusState | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const formRef = useRef<HTMLFormElement | null>(null)

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setStatus(null)
    setIsSubmitting(true)

    const formData = new FormData(event.currentTarget)

    try {
      const result = await sendContactEmail(formData)
      setStatus({ type: result.success ? "success" : "error", message: result.message })

      if (result.success) {
        formRef.current?.reset()
      }
    } catch (error) {
      console.error("Failed to submit contact form", error)
      setStatus({ type: "error", message: "Unable to send your message right now." })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section id="contact" className="relative py-24">
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-900/40 to-slate-950/80" />
        <div className="absolute left-1/2 top-0 h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-cyan-500/20 blur-[120px]" />
      </div>

      <div className="mx-auto flex w-full max-w-7xl flex-col gap-16 px-6 lg:grid lg:grid-cols-[1.1fr_1fr] lg:items-start">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="space-y-8"
        >
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-500/10 px-4 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">
              Contact us
            </div>
            <h2 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
              Let&apos;s build your next global connection.
            </h2>
            <p className="text-lg text-slate-300">
              Reach out for enterprise onboarding, media requests, or help picking the right plan. Our team replies within one business day.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            {[
              { icon: Mail, label: "Email", value: "support@connect.global" },
              { icon: Phone, label: "Phone", value: "+1 (415) 555-0190" },
              { icon: MapPin, label: "HQ", value: "San Francisco, CA" },
              { icon: Send, label: "Response", value: "Under 24 hours" },
            ].map((item) => (
              <div
                key={item.label}
                className="flex items-start gap-3 rounded-2xl border border-white/10 bg-slate-950/60 px-5 py-4 backdrop-blur"
              >
                <item.icon className="mt-1 h-5 w-5 text-cyan-300" />
                <div>
                  <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                    {item.label}
                  </div>
                  <div className="text-sm font-semibold text-white">{item.value}</div>
                </div>
              </div>
            ))}
          </div>

          <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-white/10 via-white/5 to-transparent p-6 text-sm text-slate-200">
            <div className="font-semibold text-white">Need a custom rollout?</div>
            <p className="mt-2 text-slate-300">
              We offer dedicated account management, SLA-backed uptime, and tailored device provisioning for distributed teams.
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="rounded-[32px] border border-white/10 bg-slate-950/70 p-8 shadow-[0_30px_80px_rgba(15,23,42,0.45)] backdrop-blur"
        >
          <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="space-y-2 text-sm font-medium text-slate-200">
                Name
                <input
                  name="name"
                  type="text"
                  required
                  placeholder="Your full name"
                  className="h-12 w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
                />
              </label>
              <label className="space-y-2 text-sm font-medium text-slate-200">
                Email
                <input
                  name="email"
                  type="email"
                  required
                  placeholder="you@company.com"
                  className="h-12 w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
                />
              </label>
            </div>

            <label className="space-y-2 text-sm font-medium text-slate-200">
              Subject
              <input
                name="subject"
                type="text"
                required
                placeholder="How can we help?"
                className="h-12 w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
              />
            </label>

            <label className="space-y-2 text-sm font-medium text-slate-200">
              Message
              <textarea
                name="message"
                required
                rows={5}
                placeholder="Tell us about your plans, timeline, and requirements."
                className="w-full rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
              />
            </label>

            {status && (
              <div
                role="status"
                aria-live="polite"
                className={`rounded-2xl border px-4 py-3 text-sm font-medium ${
                  status.type === "success"
                    ? "border-emerald-400/30 bg-emerald-500/10 text-emerald-200"
                    : "border-rose-400/30 bg-rose-500/10 text-rose-200"
                }`}
              >
                {status.message}
              </div>
            )}

            <Button
              type="submit"
              disabled={isSubmitting}
              className="h-12 w-full rounded-2xl bg-cyan-500 text-base font-semibold text-slate-950 transition hover:bg-cyan-400"
            >
              {isSubmitting ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent" />
                  Sending...
                </span>
              ) : (
                "Send message"
              )}
            </Button>
          </form>
        </motion.div>
      </div>
    </section>
  )
}
