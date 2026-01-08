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
                            {/* Authentic World Map Path - High Quality Mercator */}
                            <path
                                className={`transition-colors duration-500 ${isDark ? 'fill-white' : 'fill-zinc-900'}`}
                                d="M784.09,240.24c-1.89-1.92-5.46-1.56-9.15-0.74c-4.83,1.07-9.39,2.83-14.82,2.37c-3.69-0.31-7.14-2.12-10.74-2.81
                                c-3.32-0.64-6.84-0.12-10.19,0.59c-3.35,0.71-6.7,1.42-10.05,2.13c-3.57,0.76-7.22,1.23-10.66-0.36c-2.73-1.26-4.63-3.92-7.53-5.04
                                c-4.64-1.78-9.82-1.39-14.73-0.7c-4.32,0.61-8.52,1.79-12.78,2.69c-3.67,0.77-7.46,1.07-11.16,0.55c-4.22-0.59-8.15-2.6-12.38-3.08
                                c-3.41-0.39-6.93,0.3-10.33,0.85c-3.4,0.55-6.8,1.1-10.2,1.65c-2.93,0.47-5.94,0.34-8.83-0.54c-3.32-1.01-6.19-3.23-9.58-4.11
                                c-4.63-1.2-9.52-0.89-14.24-0.12c-3.92,0.64-7.72,1.96-11.63,2.58c-4.04,0.64-8.21,0.51-12.22-0.34c-4.19-0.89-8.08-3.06-12.34-3.51
                                c-4.04-0.43-8.17,0.4-12.18,1.17c-3.34,0.64-6.68,1.28-10.02,1.92c-3.1,0.6-6.31,0.42-9.35-0.65c-3.25-1.14-5.96-3.47-9.31-4.2
                                c-4.79-1.05-9.83-0.52-14.65,0.47c-3.93,0.81-7.75,2.23-11.71,2.77c-3.96,0.54-8.05,0.28-11.96-0.7c-4.14-1.04-7.85-3.4-12.06-3.72
                                c-3.83-0.29-7.72,0.72-11.48,1.65c-3.14,0.77-6.28,1.55-9.42,2.32c-2.91,0.71-5.93,0.67-8.81-0.31c-3.42-1.16-6.35-3.56-9.91-4.17
                                c-4.96-0.85-10.12,0.06-15.02,1.38c-3.79,1.02-7.44,2.69-11.33,3.08c-3.89,0.39-7.88-0.08-11.66-1.26c-3.95-1.23-7.39-3.82-11.41-4.1
                                c-3.02-0.21-6.07,0.58-9.05,1.27c-3.17,0.73-6.34,1.46-9.51,2.19c-3.26,0.75-6.66,0.66-9.83-0.46c-3.5-1.24-6.38-3.83-10.04-4.3
                                c-5.22-0.67-10.59,0.53-15.65,2.2c-3.69,1.22-7.26,3.03-11.11,3.27c-3.96,0.25-7.97-0.52-11.73-1.92c-3.85-1.43-7.11-4.18-11.12-4.27
                                c-2.99-0.07-5.99,0.95-8.91,1.96c-2.48,0.86-5.11,1.68-7.73,1.6c-4.49-0.14-8.49-2.95-12.89-3.45c-4.57-0.52-9.3,0.48-13.68,2.36
                                c-3.37,1.45-6.57,3.61-10.23,3.74c-4.06,0.14-8.13-1.07-11.83-2.85c-3.73-1.79-6.73-4.82-10.74-4.72c-2.02,0.05-4.02,0.76-5.97,1.52
                                c-2.92,1.14-5.69,2.68-8.73,3.46c-4.43,1.13-9.15,0.75-13.56-0.69c-2.3-0.75-4.48-1.83-6.8-2.52C28.23,227.1,24.97,227,21.9,228.1
                                c-1.63,0.58-3.17,1.42-4.88,1.71c-3.84,0.65-7.85-0.59-11.23-2.61c-2.26-1.35-4.15-3.32-6.56-4.26c-2.03-0.79-4.32-0.89-6.42-0.41
                                v126.85h999V228.16c-3.09-1.23-6.52-1.37-9.54,0.1c-2.73,1.33-4.99,3.58-7.93,4.42c-4.11,1.17-8.56,0.59-12.55-0.96...
                                M872.48,168.18c-2.93-0.83-6.04-0.34-8.91,0.78c-3.44,1.34-6.31,3.87-9.92,4.67c-4.96,1.1-10.16,0.02-15.02-1.48
                                c-3.66-1.13-7.14-3.03-10.99-3.35c-4.14-0.34-8.29,0.75-12.18,2.37c-3.69,1.54-6.88,4.1-10.84,4.27c-2.91,0.12-5.78-0.78-8.58-1.61
                                c-2.48-0.73-4.81-1.36-7.37-1.13c-4.73,0.42-8.91,3.54-13.52,4.32c-4.83,0.82-9.87-0.01-14.56-1.86c-3.62-1.43-6.99-3.92-10.96-4.03
                                c-3.14-0.09-6.24,0.91-9.26,1.96c-2.54,0.88-5.24,1.72-7.93,1.64c-4.49-0.14-8.49-2.95-12.89-3.45c-4.57-0.52-9.3,0.48-13.68,2.36
                                c-3.37,1.45-6.57,3.61-10.23,3.74c-4.06,0.14-8.13-1.07-11.83-2.85c-3.73-1.79-6.73-4.82-10.74-4.72c-2.02,0.05-4.02,0.76-5.97,1.52
                                z"
                                opacity="0.2"
                            />
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
