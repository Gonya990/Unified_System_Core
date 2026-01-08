"use client"

import Link from "next/link"
import { ArrowLeft, Lock } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function PrivacyPage() {
    return (
        <div className="min-h-screen bg-[#111418] text-zinc-100 font-sans p-6 md:p-12">
            <div className="max-w-4xl mx-auto">
                <Link href="/">
                    <Button variant="ghost" className="mb-8 text-zinc-400 hover:text-white pl-0">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Home
                    </Button>
                </Link>

                <div className="bg-[#1a1f26] border border-white/5 rounded-[32px] p-8 md:p-12 shadow-2xl">
                    <div className="flex items-center gap-4 mb-8 border-b border-white/5 pb-8">
                        <div className="w-12 h-12 bg-purple-500/10 rounded-2xl flex items-center justify-center">
                            <Lock className="w-6 h-6 text-purple-500" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">Privacy Policy</h1>
                            <p className="text-zinc-500 mt-1">Last updated: January 2026</p>
                        </div>
                    </div>

                    <div className="prose prose-invert prose-zinc max-w-none space-y-6 text-zinc-300">
                        <h3 className="text-xl font-bold text-white">1. Data Collection</h3>
                        <p>
                            We collect minimal personal information necessary to process your eSIM orders, including email address and payment details (processed securely by third parties).
                        </p>

                        <h3 className="text-xl font-bold text-white">2. Usage of Information</h3>
                        <p>
                            Your data is used to deliver your eSIM QR codes, send service updates, and provide customer support. We do not sell your personal data to advertisers.
                        </p>

                        <h3 className="text-xl font-bold text-white">3. Cookies</h3>
                        <p>
                            We use necessary cookies to ensure the functionality of our shopping cart and preferences (like language and currency selection).
                        </p>

                        <h3 className="text-xl font-bold text-white">4. Data Security</h3>
                        <p>
                            We implement industry-standard security measures to protect your data. All connections are encrypted via SSL.
                        </p>

                        <h3 className="text-xl font-bold text-white">5. Contact</h3>
                        <p>
                            For privacy concerns, please contact our Data Protection Officer at privacy@connect.global.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
