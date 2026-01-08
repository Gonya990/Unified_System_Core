"use client"

import Link from "next/link"
import { ArrowLeft, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function TermsPage() {
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
                        <div className="w-12 h-12 bg-blue-500/10 rounded-2xl flex items-center justify-center">
                            <FileText className="w-6 h-6 text-blue-500" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">Terms of Service</h1>
                            <p className="text-zinc-500 mt-1">Last updated: January 2026</p>
                        </div>
                    </div>

                    <div className="prose prose-invert prose-zinc max-w-none space-y-6 text-zinc-300">
                        <h3 className="text-xl font-bold text-white">1. Introduction</h3>
                        <p>
                            Welcome to Connect.Global. By accessing our website and using our eSIM services, you agree to comply with and be bound by the following terms and conditions.
                        </p>

                        <h3 className="text-xl font-bold text-white">2. Service Description</h3>
                        <p>
                            Connect.Global provides eSIM data plans for international travel. Our services are dependent on local network availability and third-party carrier agreements.
                        </p>

                        <h3 className="text-xl font-bold text-white">3. User Obligations</h3>
                        <p>
                            You agree to use our services only for lawful purposes. You are responsible for ensuring your device is eSIM compatible and unlocked before purchasing a plan.
                        </p>

                        <h3 className="text-xl font-bold text-white">4. Payment & Billing</h3>
                        <p>
                            All payments are processed securely. Prices are listed in USD/EUR/ILS and are subject to change. Plans are prepaid and activating immediately or upon installation as specified.
                        </p>

                        <h3 className="text-xl font-bold text-white">5. Limitation of Liability</h3>
                        <p>
                            Connect.Global is not liable for service interruptions caused by network operators or maintenance. Our liability is limited to the cost of the purchased plan.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
