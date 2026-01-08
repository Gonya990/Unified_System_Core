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
                            {/* Authentic World Map Path - Detailed Robinson/Mercator-like projection */}
                            <path
                                className={`transition-colors duration-500 ${isDark ? 'fill-white' : 'fill-zinc-900'}`}
                                d="M856.9,365.1c-6.8-5.3-17.2-2.3-19.6,6c-2.4,8.3-9.8,11.3-15.1,6c-5.3-5.3-1.5-16.6,6-19.6c7.5-3,8.3-14.3,1.5-19.6
                                c-6.8-5.3-17.4-4.5-22.6,1.5c-5.3,6-16.6,7.5-24.2,2.3c-7.5-5.3-9-17-3-24.2c6-7.2,16.6-9.4,24.2-4.5c7.5,4.9,19.6,3.4,25.7-3
                                c6-6.4,3.4-17.7-4.5-21.9c-7.9-4.2-18.1-1.1-23.4,6.8c-5.3,7.9-15.8,7.9-21.1,0c-5.3-7.9-1.9-19.2,6.8-22.6
                                c8.7-3.4,12.5-13.6,7.5-21.9c-4.9-8.3-15.5-11.7-24.2-7.5c-8.7,4.2-19.2,0.8-23.4-6.8c-4.2-7.5-13.2-9-21.1-3.8
                                c-7.9,5.3-18.1,2.3-22.6-6c-4.5-8.3-13.6-11.7-21.9-8.3c-8.3,3.4-17.7-1.1-21.1-9c-3.4-7.9-12.8-12.1-20.4-9.4
                                c-7.5,2.6-16.2-1.9-18.9-9.8c-2.6-7.9-9-14.3-15.1-14.3c-6,0-13.2,5.7-16.6,12.8c-3.4,7.2-12.1,10.2-18.9,6.8
                                c-6.8-3.4-15.1-0.8-18.9,5.7c-3.8,6.4-10.9,9.8-18.1,8.3c-7.2-1.5-14.7,2.3-18.1,9c-3.4,6.8-10.9,9.4-17.7,6.4
                                c-6.8-3-15.1-0.4-18.1,6c-3,6.4-10.6,8.3-16.6,4.5c-6-3.8-14.3-1.1-17.4,6c-3,7.2-9.8,11.3-17,9.4c-7.2-1.9-15.8,2.6-17.7,9.8
                                c-1.9,7.2-8.3,10.6-15.5,8.3c-7.2-2.3-14.7,0.4-17.4,6.4c-2.6,6-8.7,8.7-14.7,6c-6-2.6-12.8,0.8-15.1,7.2
                                c-2.3,6.4-9.4,8.3-15.5,4.5c-6-3.8-14,0.4-17,9c-3,8.7-10.9,11.3-18.1,6.4c-7.2-4.9-16.6-2.3-21.1,6c-4.5,8.3-13.2,10.2-20.4,4.5
                                c-7.2-5.7-17-4.5-22.6,3c-5.7,7.5-15.1,9-21.1,3.4c-6-5.7-15.8-5.3-21.9,1.1c-6,6.4-15.1,7.2-20.4,1.9c-5.3-5.3-14.3-5.3-19.6,0
                                c-5.3,5.3-13.2,6-17.7,1.5c-4.5-4.5-12.8-5.7-18.1-2.6c-5.3,3-12.5,9.4-16.2,14.7c-3.8,5.3-9.8,6.8-15.1,3.8c-5.3-3-12.1-1.5-17.4,3.8
                                c5.3,5.3-12.1,4.9-17-1.1c-4.9-6-13.6-7.5-19.6-3.8c-6,3.8-13.6,1.9-17-4.2c-3.4-6-11.7-6.8-18.9-1.5c-7.2,5.3-16.6,3-20.4-4.5
                                c-3.8-7.5-11.7-10.2-18.9-6c-7.2,4.2-16.2,2.3-19.6-4.5c-3.4-6.8-10.6-9.8-17.7-6.8c-7.2,3-14.7,0.4-17.4-6.4c-2.6-6.8-9.4-9.8-16.6-6.4
                                c-7.2,3.4-14.3,0.4-16.6-6.8c-2.3-7.2-8.3-10.6-14.7-8.3c-6.4,2.3-12.8-1.5-15.1-8.3c-2.3-6.8-7.9-9.8-14.3-7.2c-6.4,2.6-12.1-0.8-13.2-7.2
                                c-3.4,2.6-8.3,4.9-13.6,5.3c-6.8,0.4-12.1,3.8-13.2,8.7c-1.1,4.9-0.8,11.3,1.1,17c1.9,5.7,2.3,12.5,0.4,17.4c-1.9,4.9-1.5,12.1,1.1,18.1
                                c2.6,6,1.9,13.2-1.5,17.7c-3.4,4.5-4.2,11.7-1.5,17c2.6,5.3,1.9,12.1-1.5,16.2c-3.4,4.2-4.5,10.6-2.6,15.8c1.9,5.3,1.1,11.7-1.9,15.5
                                c-3,3.8-3.4,9.4-1.1,14.3c2.3,4.9,2.3,10.9-0.4,15.1c-2.6,4.2-2.6,10.2-0.4,14.7c2.3,4.5,1.9,10.2-0.8,14.3c-2.6,4.2-1.9,10.2,1.5,13.6
                                c3.4,3.4,3.4,9.4,0,13.2c-3.4,3.8-3.4,9.4,0,13.2c3.4,3.8,3.4,9.4,0,13.2c-3.4,3.8-2.6,9.4,1.5,12.5c4.2,3,5.7,8.7,3.4,13.2
                                c-2.3,4.5-1.1,10.6,2.6,13.6c3.8,3,4.5,8.7,1.9,12.8c-2.6,4.2,1.9,10.2,1.5,13.6z M164.8,114.6c-5-2.9-8.4,1.8-13.7,1.1
                                c-1.8-0.2-2.3-1.6-3.7-2.1c-3.1-1-5.3,1.4-8.2,1.3c-2.3-0.1-4.2-2.1-6.6-2.1c-2.6,0-4.9,2.8-7.9,1.8c-2-0.6-3.2-3.6-5.8-3.2
                                c-3,0.5-3.3,4.9-6.3,4.2c-3.2-0.8-3.4-6.3-7.4-5.3c-2.1,0.5-3.2,3.2-5.5,3.2c-3,0-4.7-4.1-8.2-3.4c-2.5,0.5-3.7,4.2-6.6,3.9
                                c-2-0.2-3.3-2.6-5.3-3.2c-2.3-0.6-5.3,0.3-7.1-1.3c-2.4-2.1-1.8-6.1-4.2-7.9c-1.8-1.3-4.7-1.1-6.6-2.6c-2.1-1.7,0-5.1-1.1-7.1
                                c-1-1.7-4.2-1.3-6.1-2.4c-2.1-1.3-1.8-4.7-4.2-5.5c-3-1-5.8,1.6-8.7,0c-2.4-1.3-1.8-5.3-4.5-6.3c-1.3-0.5-2.9,0.3-4.2-0.3
                                c-3-1.3-2.9-6.1-6.3-6.6c-1.8-0.3-3.2,1.1-5,0.5c-2.4-0.8-3-4.7-6.1-4.5c-2.1,0.2-3.3,2.8-5.5,2.4c-3-0.6-4.1-4.6-7.4-4.5
                                c-4.4,0.2-4.2,7.3-8.9,7.4c-2.3,0-4.1-2.1-6.6-2.4c-4.1-0.5-6.8,4.5-11.1,3.4C1.2,78.2,0.7,73.5,0,71.2v355.6l999,0V71.2
                                c-5.8,11.3-16.7,11.3-23.7,0.5c-2.1-3.2-6.8-2.6-9.2-5.3c-2.3-2.4-2.3-7.1-5.3-8.9c-2.8-1.7-5.8,1.3-8.4-0.8c-2.1-1.6-1.8-4.7-3.9-6.3
                                c-2.4-1.8-5.5-0.8-7.6-2.9c-2.1-2.1-1.1-6.3-3.4-8.2c-2.3-1.8-5.3-1.1-7.6-2.9c-1.8-1.5,0.6-5.1-0.3-7.1c-0.8-1.8-3.7-2.6-5-4.2
                                c-1.7-2.1-0.9-4.7-2.4-7.1c-1.3-2.1-4.7-2.2-6.1-4.2c-1-1.5-0.7-3.6-1.6-5c-2.1-3.2-6.2-2.1-8.4-5.3C893,1.5,887.2,4.8,883.3,0
                                H117.8c-2.5,4.3-1.7,10.6-5.8,13.7c-3.5,2.6-7.5-0.5-10.8,2.4c-2.5,2.2-2,6.4-5,8.2c-2.6,1.6-5.8-0.8-8.4,1.1
                                c-2.3,1.7-2.3,5.5-5,6.8c-2.8,1.3-5.3-1.3-7.9,0.3c-2.1,1.3-1.8,4.7-4.2,5.5c-3.8,1.3-5.7-3.4-8.9-2.6c-2.6,0.6-3.8,3.9-6.6,3.9
                                c-2,0-3.3-2.4-5.3-2.6c-2.5-0.3-4.1,2.8-6.6,1.8c-2.1-0.8-2-4.1-4.2-5c-3.6-1.5-5.6,2.8-8.9,0.8c-2.6-1.6-2.3-6.1-5.3-7.4
                                c-2.7-1.1-5.1,1.5-7.6,0.5c-1.7-0.7-2.2-2.9-3.7-3.7C8,22.2,6,23.3,4.2,22.4c-0.3-0.2-0.5-0.5-0.8-0.7v24.6
                                c2.4-1.9,4.2,2.3,7.1,0.5c3.2-2,4.8-6.4,8.7-6.8c3.6-0.3,5.4,4.6,8.9,4.2c2-0.2,3.3-2.6,5.3-3.2c2.3-0.6,5.3,0.3,7.1-1.3
                                c2.4-2.1,1.8-6.1,4.2-7.9c2.3-1.7,5.1-0.2,7.4-2.1c2.2-1.8,1.7-5.5,4.2-6.8c2.9-1.5,5.6,1.7,8.2,0.3c2-1.1,1.5-4.5,3.2-6.1
                                c2.1-2,5.6-0.7,7.6-2.9c1.5-1.6,1.4-4,2.9-5.5c2.1-2.1,5.3-1.1,7.4-3.2c1.7-1.7,1.8-4.4,3.7-5.8c2.6-2,6-0.6,8.4-2.9
                                c1.8-1.7,2.2-4.6,4.2-5.8c2.8-1.7,5.5,1.2,7.9-0.5c1.8-1.3,1.9-4,3.7-5c2.4-1.3,4.6,0.9,6.8-0.5c1.8-1.1,1.9-3.8,3.9-4.5
                                c3.5-1.2,5.4,3.6,8.7,1.8c2.3-1.2,2.2-4.8,4.7-5.5c3-0.8,4.8,2.8,7.6,1.6c2.5-1.1,2.8-4.9,5.5-5.3c3-0.4,4.4,3.6,7.4,2.6
                                c2.5-0.8,3-4.6,5.8-4.7c2.9-0.1,4.3,4,7.1,3.4c2.8-0.6,3.4-4.8,6.3-4.7c2.6,0,3.9,3.6,6.6,3.2c2.2-0.3,3-3.3,5.3-3.4
                                c2.6-0.1,3.9,3.6,6.6,3.2c2.2-0.3,3-3.3,5.3-3.4c2.9-0.1,4.3,4,7.1,3.4c2.5-0.5,3.2-4.3,5.8-4.2c3.3,0.1,4.9,4.5,8.2,3.9
                                c2.3-0.4,3.1-3.6,5.5-3.4c3.4,0.3,4.8,5.1,8.4,4.5c2.6-0.5,3.5-3.8,6.1-3.7c3.2,0.2,4.7,4.7,7.9,4.2c2.5-0.4,3.3-3.7,5.8-3.4
                                c2.9,0.3,4.1,4.4,7.1,4.2c3.2-0.2,4.7-4.7,7.9-4.2c2.5-0.4,3.3-3.7,5.8-3.4c3.3,0.4,4.8,5,8.2,4.5c2.6-0.4,3.5-3.8,6.1-3.7
                                c3.4,0.2,4.9,4.8,8.4,4.2c2.4-0.4,3.2-3.6,5.5-3.4c3.4,0.3,4.8,5.1,8.4,4.5c2.6-0.5,3.5-3.8,6.1-3.7c0.1,0,0.3,0,0.4,0
                                c3.7,0.2,5.5,5.2,9.2,4.7c2.3-0.3,3.3-3.3,5.5-3.2c3,0.2,4.3,4.3,7.1,4.2c2.7-0.1,3.8-3.9,6.6-3.4
                                C162.7,110.4,163.5,113.8,164.8,114.6z"
                                opacity="0.3"
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
