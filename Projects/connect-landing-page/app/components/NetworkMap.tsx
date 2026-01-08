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

export default function NetworkMap({ t }: { t: Translation }) {
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

    return (
        <section id="network" className="py-24 relative overflow-hidden bg-zinc-950">
            {/* Background Glows */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-blue-500/10 blur-[120px] rounded-full -z-10" />
            <div className="absolute top-1/2 left-1/4 -translate-y-1/2 w-[400px] h-[200px] bg-purple-500/10 blur-[100px] rounded-full -z-10" />

            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold uppercase tracking-widest mb-6"
                    >
                        <Activity className="w-4 h-4 animate-pulse" />
                        Live Network Status
                    </motion.div>
                    <h2 className="text-4xl md:text-5xl font-black mb-6 tracking-tight text-white">
                        {network.title}
                    </h2>
                    <p className="text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed">
                        {network.subtitle}
                    </p>
                </div>

                {/* Map Container */}
                <div className="relative aspect-[2/1] w-full rounded-[48px] border border-white/5 bg-zinc-900/50 backdrop-blur-3xl overflow-hidden shadow-2xl">
                    {/* SVG World Map Placeholder (Simplified) */}
                    <svg
                        viewBox="0 0 1000 500"
                        className="w-full h-full opacity-20 pointer-events-none"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="0.5"
                    >
                        <path
                            className="text-white"
                            d="M150,150 L200,160 L240,140 L280,150 L300,180 L280,220 L240,240 L200,230 L160,200 Z"
                            fill="currentColor"
                            opacity="0.1"
                        />
                        {/* Realistically, would use a complete GeoJSON d-path, but simplified for aesthetic */}
                        <circle cx="500" cy="250" r="240" strokeDasharray="10 10" opacity="0.2" />
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
                            <div className={`absolute bottom-full left-1/2 -translate-x-1/2 mb-4 p-4 rounded-2xl bg-zinc-900/90 border border-white/10 backdrop-blur-xl shadow-2xl min-w-[200px] transition-all duration-300 pointer-events-none z-50 ${hoveredNode?.id === node.id ? 'opacity-100 translate-y-0 scale-100' : 'opacity-0 translate-y-2 scale-95'}`}>
                                <div className="flex items-center justify-between mb-2">
                                    <span className="font-bold text-sm text-white">{node.name}</span>
                                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-green-500/10 text-green-400 font-black">ONLINE</span>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <div className="text-[8px] uppercase font-black tracking-widest text-zinc-500">{network.node_latency}</div>
                                        <div className="text-xs font-bold text-blue-400">{node.latency}</div>
                                    </div>
                                    <div>
                                        <div className="text-[8px] uppercase font-black tracking-widest text-zinc-500">Load</div>
                                        <div className="text-xs font-bold text-purple-400">{node.load}%</div>
                                    </div>
                                </div>
                                <div className="mt-2 w-full h-1 bg-white/5 rounded-full overflow-hidden">
                                    <motion.div
                                        className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                                        initial={{ width: 0 }}
                                        animate={{ width: `${node.load}%` }}
                                    />
                                </div>
                            </div>
                        </motion.div>
                    ))}

                    {/* Stats Overlay (Glass) */}
                    <div className="absolute bottom-8 left-8 right-8 md:right-auto md:w-80 p-8 rounded-[32px] border border-white/10 bg-black/40 backdrop-blur-2xl shadow-2xl flex flex-col gap-6">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center">
                                <Globe className="w-6 h-6 text-blue-500" />
                            </div>
                            <div>
                                <div className="text-[10px] uppercase font-black tracking-widest text-zinc-500">{network.active_nodes}</div>
                                <div className="text-2xl font-black text-white tabular-nums">
                                    {activeNodes.toLocaleString()}
                                </div>
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 flex items-center justify-center">
                                <Database className="w-6 h-6 text-purple-500" />
                            </div>
                            <div>
                                <div className="text-[10px] uppercase font-black tracking-widest text-zinc-500">{network.global_traffic}</div>
                                <div className="text-2xl font-black text-white tabular-nums">
                                    {traffic} <span className="text-sm opacity-50">PB/s</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-2xl bg-green-500/10 flex items-center justify-center">
                                <Zap className="w-6 h-6 text-green-500" />
                            </div>
                            <div>
                                <div className="text-[10px] uppercase font-black tracking-widest text-zinc-500">{network.uptime_guarantee}</div>
                                <div className="text-2xl font-black text-white">99.99%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}
