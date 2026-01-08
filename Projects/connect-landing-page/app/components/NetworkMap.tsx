"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { Globe, Database, Zap, Activity } from "lucide-react"

import { Translation } from "@/app/data/translations"

interface Node {
    id: number
    x: number
    y: number
    name: string
    latency: string
    load: number
}

const NODES: Node[] = [
    { id: 1, x: 150, y: 180, name: "San Francisco", latency: "12ms", load: 65 },
    { id: 2, x: 280, y: 185, name: "New York", latency: "18ms", load: 42 },
    { id: 3, x: 485, y: 145, name: "London", latency: "14ms", load: 88 },
    { id: 4, x: 510, y: 150, name: "Frankfurt", latency: "16ms", load: 74 },
    { id: 5, x: 585, y: 205, name: "Tel Aviv", latency: "8ms", load: 92 },
    { id: 6, x: 620, y: 235, name: "Dubai", latency: "22ms", load: 55 },
    { id: 7, x: 765, y: 325, name: "Singapore", latency: "28ms", load: 48 },
    { id: 8, x: 865, y: 185, name: "Tokyo", latency: "32ms", load: 61 },
    { id: 9, x: 885, y: 425, name: "Sydney", latency: "42ms", load: 35 },
    { id: 10, x: 345, y: 385, name: "São Paulo", latency: "38ms", load: 29 },
    { id: 11, x: 535, y: 425, name: "Cape Town", latency: "45ms", load: 15 },
    { id: 12, x: 685, y: 265, name: "Mumbai", latency: "24ms", load: 44 },
]

export default function NetworkMap({ t, theme }: { t: Translation, theme: "dark" | "light" }) {
    const [activeNodes, setActiveNodes] = useState(1420)
    const [traffic, setTraffic] = useState(84.2)
    const [hoveredNode, setHoveredNode] = useState<Node | null>(null)

    useEffect(() => {
        const interval = setInterval(() => {
            setActiveNodes(prev => prev + (Math.random() > 0.5 ? 1 : -1))
            setTraffic(prev => {
                const next = prev + (Math.random() - 0.5) * 0.5
                return parseFloat(next.toFixed(1))
            })
        }, 3000)
        return () => clearInterval(interval)
    }, [])

    const network = t.network;
    if (!network) return <></>;

    const isDark = theme === 'dark';

    return (
        <section id="network" className={`py-24 relative overflow-hidden transition-colors duration-500 ${isDark ? 'bg-zinc-950' : 'bg-[#e0e5ec]'}`}>
            {/* Background Glows */}
            <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] blur-[120px] rounded-full -z-10 transition-colors duration-500 ${isDark ? 'bg-blue-500/10' : 'bg-blue-500/5'}`} />
            <div className={`absolute top-1/2 left-1/4 -translate-y-1/2 w-[400px] h-[200px] blur-[100px] rounded-full -z-10 transition-colors duration-500 ${isDark ? 'bg-purple-500/10' : 'bg-purple-500/5'}`} />

            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border text-xs font-bold uppercase tracking-widest mb-6 ${isDark ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' : 'bg-blue-500/10 border-blue-500/20 text-blue-600'}`}
                    >
                        <Activity className="w-4 h-4 animate-pulse" />
                        Live Network Status
                    </motion.div>
                    <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${isDark ? 'from-white via-blue-100 to-blue-400' : 'from-zinc-900 via-zinc-800 to-blue-600'}`}>
                            {network.title}
                        </span>
                    </h2>
                    <p className={`text-xl max-w-2xl mx-auto leading-relaxed transition-colors duration-500 ${isDark ? 'text-zinc-400' : 'text-zinc-600'}`}>
                        {network.subtitle}
                    </p>
                </div>

                {/* Map Container - Flex-col on mobile, regular block on desktop */}
                <div className={`relative w-full rounded-[48px] border overflow-hidden shadow-2xl transition-all duration-500 flex flex-col md:block md:h-[600px] ${isDark ? 'border-white/5 bg-zinc-900/50 backdrop-blur-3xl' : 'border-white/40 bg-white/60 backdrop-blur-xl'}`}>
                    {/* SVG World Map Placeholder */}
                    <div className="relative w-full aspect-[2/1] md:h-full md:absolute md:inset-0" suppressHydrationWarning>
                        <svg
                            viewBox="0 0 1000 500"
                            className="w-full h-full pointer-events-none"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="0.5"
                        >
                            {/* Authentic World Map - Verified Multi-Path Structure */}
                            <g className={`transition-colors duration-500 ${isDark ? 'fill-white' : 'fill-zinc-900'}`} opacity="0.15">
                                {/* North America */}
                                <path d="M165.5,126.3c-2.8-4.7-8.3-6.4-13.3-6.9c-7.2-0.7-14.7,2.2-19.4,7.8c-3.1,3.6-4.2,8.6-3.1,13.3c1.9,8.6,10.3,14.4,18.9,13.6c5.8-0.6,11.1-4.2,13.3-9.4C164.7,138.9,165.8,131.9,165.5,126.3z M98.3,116.7c-5.8-5.3-14.4-6.4-21.4-2.8c-5.3,2.8-8.6,8.6-8.3,14.7c0.3,7.5,6.7,13.9,14.2,14.2c6.1,0.3,11.9-3.1,14.7-8.3C100.8,128.6,101.9,121.1,98.3,116.7z M250,75l-20,10l10,20l-15,15l-35-10l-10,25l20,30l-15,20l10,20l45,5l25-25l10-40l-15-20L250,75z" />

                                {/* South America */}
                                <path d="M310,280l-30,20l-10,40l15,60l35,45l30-20l20-70l-20-50L310,280z" />

                                {/* Europe & Africa */}
                                <path d="M480,110l-20,10l-10,25l15,15l-5,25l-30,30l10,35l-20,40l30,60l50,20l40-30l10-60l-20-40l30-30l-10-30l-30-10l-20-40L480,110z" />

                                {/* Asia */}
                                <path d="M650,90l-30,30l10,40l-20,30l30,30l10,40l40,20l30,30l30-20l10-40l30-20l20,10l20-40l-30-40l-50-20l-60,10L650,90z" />

                                {/* Australia */}
                                <path d="M850,350l-30,10l-10,30l20,30l50,10l30-20l-10-40L850,350z" />

                                {/* Islands (Indonesia, Japan, UK, etc) - Simplified */}
                                <circle cx="500" cy="100" r="8" />
                                <circle cx="880" cy="180" r="10" />
                                <circle cx="780" cy="300" r="12" />
                                <circle cx="920" cy="400" r="10" />
                            </g>
                        </svg>

                        {/* Node Connections (Animated Lines) */}
                        <svg viewBox="0 0 1000 500" className="absolute inset-0 w-full h-full pointer-events-none">
                            {NODES.filter(n => n.id !== 5).map((node, i) => (
                                <motion.path
                                    key={i}
                                    d={`M 585 205 Q ${(585 + node.x) / 2} ${(205 + node.y) / 2 - 50} ${node.x} ${node.y}`}
                                    stroke="url(#lineGradient)"
                                    strokeWidth="1"
                                    fill="none"
                                    initial={{ pathLength: 0, opacity: 0 }}
                                    animate={{ pathLength: 1, opacity: 0.2 }}
                                    transition={{ duration: 2, delay: i * 0.1 }}
                                />
                            ))}
                            <defs>
                                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" stopColor="#3b82f6" stopOpacity="0" />
                                    <stop offset="50%" stopColor="#3b82f6" stopOpacity="1" />
                                    <stop offset="100%" stopColor="#a855f7" stopOpacity="0" />
                                </linearGradient>
                            </defs>
                        </svg>

                        {/* Active Node Points */}
                        {NODES.map((node) => (
                            <motion.div
                                key={node.id}
                                className="absolute group cursor-crosshair"
                                style={{ left: `${node.x / 10}%`, top: `${node.y / 5}%` }}
                                onMouseEnter={() => setHoveredNode(node)}
                                onMouseLeave={() => setHoveredNode(null)}
                                initial={{ scale: 0 }}
                                whileInView={{ scale: 1 }}
                                whileHover={{ scale: 1.5 }}
                            >
                                <div className="relative">
                                    <div className="absolute -inset-4 bg-blue-500/20 blur-xl rounded-full scale-0 group-hover:scale-100 transition-transform duration-500" />
                                    <div className="w-3 h-3 bg-blue-500 rounded-full border-2 border-white/20 shadow-[0_0_15px_rgba(59,130,246,0.8)]" />
                                    <div className="absolute inset-0 w-3 h-3 bg-blue-400 rounded-full animate-ping opacity-75" />
                                </div>

                                {/* Tooltip */}
                                <div className={`absolute bottom-full left-1/2 -translate-x-1/2 mb-4 p-4 rounded-2xl border backdrop-blur-xl shadow-2xl min-w-[200px] transition-all duration-300 pointer-events-none z-50 ${hoveredNode?.id === node.id ? 'opacity-100 translate-y-0 scale-100' : 'opacity-0 translate-y-2 scale-95'} ${isDark ? 'bg-zinc-900/90 border-white/10' : 'bg-white/90 border-zinc-200'}`}>
                                    <div className="flex items-center justify-between mb-2">
                                        <span className={`font-bold text-sm ${isDark ? 'text-white' : 'text-zinc-900'}`}>{node.name}</span>
                                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 font-black">ONLINE</span>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <div className={`text-[8px] uppercase font-black tracking-widest ${isDark ? 'text-zinc-500' : 'text-zinc-400'}`}>{network.node_latency}</div>
                                            <div className="text-xs font-bold text-blue-500">{node.latency}</div>
                                        </div>
                                        <div>
                                            <div className={`text-[8px] uppercase font-black tracking-widest ${isDark ? 'text-zinc-500' : 'text-zinc-400'}`}>Load</div>
                                            <div className="text-xs font-bold text-purple-500">{node.load}%</div>
                                        </div>
                                    </div>
                                    <div className={`mt-2 w-full h-1 rounded-full overflow-hidden ${isDark ? 'bg-white/5' : 'bg-black/5'}`}>
                                        <motion.div
                                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                                            initial={{ width: 0 }}
                                            animate={{ width: `${node.load}%` }}
                                        />
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    {/* Stats Overlay (Glass) - Relative on mobile, Absolute on desktop */}
                    <div className={`relative p-8 md:absolute md:bottom-8 md:left-8 md:right-auto md:w-80 rounded-[32px] border backdrop-blur-2xl shadow-2xl flex flex-col gap-6 ${isDark ? 'bg-black/40 border-white/10' : 'bg-white/80 border-white/40'}`}>
                        <div className="flex items-center gap-4">
                            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${isDark ? 'bg-blue-500/10' : 'bg-blue-500/10'}`}>
                                <Globe className="w-6 h-6 text-blue-500" />
                            </div>
                            <div>
                                <div className={`text-[10px] uppercase font-black tracking-widest ${isDark ? 'text-zinc-500' : 'text-zinc-500'}`}>{network.active_nodes}</div>
                                <div suppressHydrationWarning className={`text-2xl font-black tabular-nums ${isDark ? 'text-white' : 'text-zinc-900'}`}>
                                    {activeNodes.toLocaleString('en-US')}
                                </div>
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${isDark ? 'bg-purple-500/10' : 'bg-purple-500/10'}`}>
                                <Database className="w-6 h-6 text-purple-500" />
                            </div>
                            <div>
                                <div className={`text-[10px] uppercase font-black tracking-widest ${isDark ? 'text-zinc-500' : 'text-zinc-500'}`}>{network.global_traffic}</div>
                                <div suppressHydrationWarning className={`text-2xl font-black tabular-nums ${isDark ? 'text-white' : 'text-zinc-900'}`}>
                                    {traffic} <span className="text-sm opacity-50">PB/s</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${isDark ? 'bg-green-500/10' : 'bg-green-500/10'}`}>
                                <Zap className="w-6 h-6 text-green-500" />
                            </div>
                            <div>
                                <div className={`text-[10px] uppercase font-black tracking-widest ${isDark ? 'text-zinc-500' : 'text-zinc-500'}`}>{network.uptime_guarantee}</div>
                                <div className={`text-2xl font-black ${isDark ? 'text-white' : 'text-zinc-900'}`}>99.99%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
