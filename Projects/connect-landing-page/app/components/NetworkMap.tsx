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
                            {/* Authentic World Map Path - Simplified Standard Projection */}
                            {/* Authentic World Map Path - Simplified Standard Projection */}
                            <path
                                className={`transition-colors duration-500 ${isDark ? 'fill-white' : 'fill-zinc-900'}`}
                                d="M843.3,348.6c-4.8,0-8.9,0.7-12.7,2.2c-3.1,1.2-5.7,2.8-8,4.9c-1.9,1.7-4.1,4.4-4.8,6.8c-1.6,5.8-0.6,13.7,2.6,18.4c1.1,1.6,2.3,2.8,3,3.1
                                c0.5,0.2,1,0.2,1.3-0.2c0.2-0.2,0.2-0.6-0.1-1.3c-1.3-3.1-2.4-9.3-0.8-13.8c0.7-2,2.8-4.5,4.6-6c2.1-1.8,4.5-3.2,7.2-4.2
                                c3.4-1.3,7-1.9,11.3-1.9c0.8,0,1.5-0.6,1.5-1.5S844.1,348.6,843.3,348.6z M796,307.3c-2,0-3.9,0.5-5.6,1.4c-3.5,1.9-5.4,5.4-4.9,9.2
                                c0.5,3.9,3.1,6.8,7.9,8.7c3.3,1.3,7.5,1.9,12.4,1.8c0.8,0,1.5-0.7,1.5-1.5c0-0.8-0.6-1.5-1.5-1.5c-4.7,0.1-8.5-0.5-11.4-1.6
                                c-3.5-1.4-5.2-3.3-5.5-5.5c-0.2-2.1,0.8-4.2,3-5.4c1.1-0.6,2.5-1,4-1c0.8,0,1.5-0.7,1.5-1.5S796.8,307.3,796,307.3z M631,136.6
                                c-2,0.3-4.1,1.1-5.9,2.4c-3.3,2.4-4.9,6.1-4.2,9.7c0.8,3.9,3.8,6.6,8.2,7.3c0.4,0.1,0.9,0.1,1.3,0.1c3.8,0,7.9-1.2,11.7-3.4
                                c0.7-0.4,0.9-1.3,0.5-2c-0.4-0.7-1.3-0.9-2-0.5c-3.4,2-7,3-10.4,2.9c-3.3-0.5-5.4-2.3-5.9-4.9c-0.4-2.3,0.6-4.6,2.8-6.1
                                c1.2-0.8,2.6-1.3,3.9-1.5c0.8-0.1,1.4-0.9,1.2-1.7C632.2,137.2,631.8,136.5,631,136.6z M551.4,98.2c-4.2,0.8-8,3.7-9.5,7.9
                                c-1.6,4.5-0.5,10.2,2.8,15.1c5,7.4,15.2,11.1,23.3,13.6c5,1.5,9.4,2.4,10.1,2.5c0.8,0.2,1.6-0.3,1.7-1.1c0.2-0.8-0.3-1.6-1.1-1.7
                                c-0.6-0.1-4.8-1-9.5-2.4c-7.3-2.3-16.5-5.6-20.9-12.1c-2.6-3.8-3.3-8.1-2-11.6c1.1-3,3.8-5,6.8-5.6c0.8-0.2,1.3-0.9,1.2-1.7
                                C552.1,98.3,551.4,98.2,551.4,98.2z M479.2,242.9c-0.5,0.7-0.9,1.5-1.2,2.3c-2.4,7.2,2.1,14.6,8.6,18.4c3.4,2,7.5,3,11.6,2.9
                                c4.4-0.1,8.9-1.5,12.7-3.9c0.7-0.4,0.9-1.3,0.5-2c-0.4-0.7-1.3-0.9-2-0.5c-3.4,2.2-7.4,3.4-11.3,3.5c-3.5,0.1-7-0.7-9.8-2.4
                                c-5.2-3-8.6-8.8-6.7-14.4c0.2-0.7,0.5-1.3,0.9-1.9c0.5-0.7,0.3-1.6-0.3-2C481.4,242.3,479.7,242.2,479.2,242.9z M308.5,395.9
                                c-2,0.4-3.9,1.5-5.4,3.2c-2.7,3-3.1,7.5-1,11c1.9,3.1,5.3,4.9,8.7,4.6c4.2-0.3,8.4-3.3,11.7-7.7c0.5-0.6,0.4-1.6-0.2-2.1
                                c-0.6-0.5-1.6-0.4-2.1,0.2c-2.9,3.8-6.4,6.4-9.6,6.6c-2.4,0.2-4.6-0.9-5.9-3c-1.3-2.2-1-5,0.7-6.9c0.9-1.1,2.1-1.7,3.4-2
                                c0.8-0.2,1.3-0.9,1.1-1.7C309.8,397.3,309.3,395.7,308.5,395.9z M287.4,260.6c-2.9,0.2-5.7,1.8-7.5,4.6c-3.2,5-2.2,11.6,2.4,16.1
                                c2.3,2.2,5.3,3.4,8.4,3.4c2.8,0,5.6-1,8.1-2.9c0.6-0.5,0.8-1.4,0.3-2c-0.5-0.6-1.4-0.8-2-0.3c-2,1.5-4.2,2.2-6.4,2.2
                                c-2.3,0-4.5-0.9-6.1-2.5c-3.5-3.4-4.2-8.3-1.8-12.1c1.4-2.1,3.4-3.3,5.6-3.4c0.8,0,1.5-0.7,1.5-1.5S288.2,260.5,287.4,260.6z
                                 M168,168.8c-2.4,0.7-4.6,2.5-6.1,5.1c-2.7,4.8-1.7,10.8,2.4,14.6c3.9,3.6,9.5,4.9,14.7,3.5c4.7-1.3,9.7-5.7,13.8-11.4
                                c0.5-0.7,0.3-1.6-0.3-2.1c-0.7-0.5-1.6-0.3-2.1,0.3c-3.7,5.2-8.1,9.1-12.2,10.2c-4.1,1.1-8.5,0.1-11.5-2.7c-3.1-2.9-3.9-7.4-1.9-11
                                c1.2-2,2.8-3.3,4.6-3.8c0.8-0.2,1.3-1,1.1-1.8C170.3,168.9,169.1,168.5,168,168.8z M65,123.6c-3.6,1.4-6.4,4.5-7.5,8.8
                                c-1.6,6.3,0.7,13.7,5.3,18.3c0.6,0.6,1.4,1.1,2.4,1.5c4.1,1.6,9.1,0.8,13.5-1.8c0.7-0.4,0.9-1.3,0.5-2c-0.4-0.7-1.3-0.9-2-0.5
                                c-3.5,2.1-7.4,2.7-10.4,1.6c-0.6-0.2-1.1-0.6-1.5-1c-3.6-3.6-5.3-9.1-4.1-13.8c0.8-3.1,2.8-5.3,5.4-6.3c0.8-0.3,1.2-1.1,0.9-1.9
                                C67.2,124,66.2,123.2,65,123.6z"
                                opacity="0.15"
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
