"use client"

import { useState } from "react"
import { ChevronDown } from "lucide-react"

const faqs = [
  {
    question: "How do I start connecting with people?",
    answer:
      "Simply select your destination from our destination selector or browse our popular destinations list. Once you've chosen your location, you can start exploring connections in that area.",
  },
  {
    question: "Is the service available worldwide?",
    answer:
      "Yes! We operate in over 190 countries and regions worldwide. Our platform is designed to connect people across the globe, no matter where you are.",
  },
  {
    question: "How secure is my information?",
    answer:
      "We take your privacy and security seriously. All data is encrypted end-to-end, and we never share your personal information with third parties without your explicit consent.",
  },
  {
    question: "Can I connect with businesses as well as individuals?",
    answer:
      "Our platform supports both personal and professional connections. You can network with individuals, families, and businesses across the world.",
  },
  {
    question: "What makes your platform different?",
    answer:
      "We focus on meaningful connections that matter. Our innovative technology combined with a human-first approach ensures that every connection you make is valuable and authentic.",
  },
]

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  return (
    <section className="py-20 px-6 bg-muted/30">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">Frequently Asked Questions</h2>
          <p className="text-muted-foreground text-lg">Everything you need to know about our platform</p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div key={index} className="bg-card border border-border rounded-lg overflow-hidden">
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-muted/50 transition-colors"
              >
                <span className="font-semibold text-card-foreground pr-4">{faq.question}</span>
                <ChevronDown
                  className={`w-5 h-5 text-muted-foreground flex-shrink-0 transition-transform ${
                    openIndex === index ? "rotate-180" : ""
                  }`}
                />
              </button>
              <div
                className={`overflow-hidden transition-all duration-300 ${
                  openIndex === index ? "max-h-96" : "max-h-0"
                }`}
              >
                <div className="px-6 pb-4 pt-2 text-muted-foreground leading-relaxed">{faq.answer}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
