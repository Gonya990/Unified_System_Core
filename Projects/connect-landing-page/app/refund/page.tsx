"use client"

import Link from "next/link"
import { ArrowLeft, RefreshCcw } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function RefundPage() {
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
                        <div className="w-12 h-12 bg-green-500/10 rounded-2xl flex items-center justify-center">
                            <RefreshCcw className="w-6 h-6 text-green-500" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold">Refund Policy</h1>
                            <p className="text-zinc-500 mt-1">Last updated: January 2026</p>
                        </div>
                    </div>

                    <div className="prose prose-invert prose-zinc max-w-none space-y-6 text-zinc-300">
                        <h3 className="text-xl font-bold text-white">1. Eligibility</h3>
                        <p>
                            We offer refunds for eSIM plans that have <strong>not been installed or activated</strong>. Once an eSIM is installed on a device, it is considered &quot;used&quot; and cannot be refunded.
                        </p>

                        <h3 className="text-xl font-bold text-white">2. Technical Issues</h3>
                        <p>
                            If you experience technical issues that Connect.Global support cannot resolve, we may issue a full or partial refund at our discretion, even if the eSIM was installed.
                        </p>

                        <h3 className="text-xl font-bold text-white">3. Request Process</h3>
                        <p>
                            To request a refund, please contact support@connect.global with your order ID within 30 days of purchase.
                        </p>

                        <h3 className="text-xl font-bold text-white">4. Processing Time</h3>
                        <p>
                            Approved refunds are processed within 5-10 business days and returned to the original payment method.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
