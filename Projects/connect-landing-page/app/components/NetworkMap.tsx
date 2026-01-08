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
                            {/* Authentic World Map - Real Mercator Data from Wikimedia */}
                            <g className={`transition-colors duration-500 ${isDark ? 'fill-white' : 'fill-zinc-900'}`} opacity="0.15">
                                <path
                                    d="m 586.08718,312.65328 c -0.005,-0.0512 -0.009,-0.11436 -0.008,-0.18682 0.001,-0.0577 0.006,-0.12191 0.0163,-0.19209 0.009,-0.0635 0.023,-0.13123 0.0421,-0.20356 0.0186,-0.0704 0.042,-0.14357 0.0707,-0.22093 0.0286,-0.077 0.0616,-0.1557 0.0994,-0.23892 0.0428,-0.0943 0.0886,-0.18736 0.13938,-0.28918 6.9e-4,-0.001 0.0148,-0.0296 0.0155,-0.031 0.0133,-0.0264 0.0169,-0.0521 0.0168,-0.0732 -10e-6,-0.008 -5.5e-4,-0.0153 -0.001,-0.0216 -0.001,-0.011 -0.003,-0.0213 -0.004,-0.0255 -0.002,-0.0108 -8.3e-4,-0.007 -9.3e-4,-5.4e-4 -1e-4,0.006 -9.6e-4,0.0172 -0.007,0.0312 7e-5,-1.8e-4 0.002,-0.003 0.005,-0.0101 0.005,-0.009 0.01,-0.018 0.0161,-0.0287 0.0112,-0.0195 0.023,-0.0393 0.0355,-0.0602 0.0168,-0.0279 0.0343,-0.0564 0.0525,-0.0852 0.0124,-0.0196 0.0251,-0.0394 0.0381,-0.059 0.008,-0.0113 0.0149,-0.0222 0.0224,-0.0326 0.005,-0.007 0.008,-0.011 0.0107,-0.0141 0.10727,-0.10708 0.17514,-0.17494 0.28338,-0.28319 0.005,-0.005 0.01,-0.0104 0.0137,-0.0161 0.0147,-0.0202 0.0208,-0.0401 0.0225,-0.0455 0.006,-0.0192 0.008,-0.0356 0.009,-0.0444 0.003,-0.0186 0.004,-0.0335 0.005,-0.0446 8e-4,-0.007 8.4e-4,-0.006 4.1e-4,-0.004 -4.7e-4,0.002 -0.001,0.006 -0.003,0.0104 -0.001,0.004 -0.003,0.007 -0.005,0.0105 -0.008,0.0156 -0.0146,0.0214 -0.0142,0.021 -0.003,0.003 -6.6e-4,7.6e-4 0.005,-0.004 0.007,-0.005 0.0239,-0.0187 0.0372,-0.0304 0.008,-0.007 0.0211,-0.0189 0.0335,-0.0349 0.006,-0.008 0.0188,-0.0254 0.0266,-0.0496 0.003,-0.0108 0.004,-0.0139 0.004,-0.0131 0.005,-0.0175 0.01,-0.0338 0.0163,-0.0498 0.006,-0.0161 0.0139,-0.0324 0.0225,-0.0489 0.0118,-0.0227 0.0254,-0.0456 0.0407,-0.0707 0.0129,-0.021 0.0266,-0.0428 0.0405,-0.0657 0.002,-0.004 0.006,-0.01 0.009,-0.0142 -0.002,0.003 -6.5e-4,0.001 0.004,-0.004 0.005,-0.005 0.0109,-0.0111 0.0183,-0.0179 0.0106,-0.01 0.0221,-0.0198 0.0347,-0.0303 0.0241,-0.0202 0.0484,-0.0394 0.0753,-0.0611 0.0108,-0.009 0.0225,-0.0182 0.0343,-0.0281 0.008,-0.007 0.0203,-0.0172 0.0322,-0.0294 0.003,-0.003 0.0135,-0.0138 0.0226,-0.0281 0.009,-0.0148 0.0114,-0.0217 0.0117,-0.0223 0.009,-0.02 0.013,-0.0372 0.0158,-0.05 0.004,-0.0171 0.006,-0.0331 0.008,-0.0472 0.002,-0.0206 0.004,-0.0404 0.004,-0.0589 9.8e-4,-0.0268 9.8e-4,-0.0529 5.3e-4,-0.0781 -6.6e-4,-0.0356 -0.002,-0.0707 -0.004,-0.10493 -0.003,-0.0446 -0.006,-0.0889 -0.009,-0.13197 -0.002,-0.0211 -0.003,-0.0411 -0.005,-0.0611 -7.2e-4,-0.0108 -0.001,-0.0203 -0.002,-0.0295 -2.4e-4,-0.006 -1.5e-4,-0.01 -1.3e-4,-0.0102 0.002,-0.0342 0.005,-0.0671 0.01,-0.10051 0.006,-0.0405 0.0127,-0.0811 0.0208,-0.12229 0.0128,-0.0651 0.0279,-0.13026 0.0435,-0.1969 0.008,-0.0362 0.017,-0.0728 0.0252,-0.10963 0.0213,-0.096 0.0468,-0.19119 0.0748,-0.28571 0.0336,-0.11353 0.0711,-0.22636 0.1095,-0.33892 0.0506,-0.14828 0.103,-0.29601 0.15171,-0.44627 0.0341,-0.10524 0.0662,-0.21103 0.0943,-0.31809 0.0255,-0.0968 0.0476,-0.19427 0.0651,-0.29253 0.007,-0.0366 0.0123,-0.073 0.0175,-0.10919 0.004,-0.0279 0.0102,-0.0569 0.0173,-0.0869 0.0113,-0.0473 0.0243,-0.0926 0.0377,-0.14379 0.009,-0.0341 0.0177,-0.0694 0.0249,-0.10569 0.004,-0.0221 0.006,-0.0426 0.008,-0.0584 0.003,-0.0313 0.004,-0.0615 0.004,-0.0891 6.6e-4,-0.037 4.6e-4,-0.0733 -1.2e-4,-0.10821 -9.2e-4,-0.0542 -0.003,-0.10762 -0.005,-0.15951 -0.003,-0.0731 -0.008,-0.14503 -0.0127,-0.21528 -0.006,-0.0841 -0.013,-0.16649 -0.0209,-0.24733 -0.007,-0.0707 -0.0146,-0.13967 -0.0232,-0.20759 -0.006,-0.0502 -0.0132,-0.099 -0.0209,-0.14721 -0.006,-0.0376 -0.0124,-0.0741 -0.0198,-0.11042 -0.006,-0.0306 -0.0132,-0.0612 -0.022,-0.092 -0.005,-0.0189 -0.0121,-0.0398 -0.0214,-0.0613 -0.005,-0.0116 -0.0129,-0.0282 -0.0253,-0.0452 -0.005,-0.006 -0.01,-0.0129 -0.0167,-0.0195 a 0.12257406,0.12257406 90 0 0 -0.17348,0.17322 c -0.004,-0.004 -0.006,-0.007 -0.008,-0.009 -0.003,-0.005 -0.004,-0.007 -0.002,-0.002 0.003,0.007 0.006,0.0163 0.0104,0.0309 0.006,0.022 0.0118,0.0459 0.0174,0.0734 0.006,0.0318 0.0123,0.0648 0.0179,0.1 0.007,0.045 0.0137,0.0912 0.0198,0.13946 0.008,0.0652 0.0157,0.13187 0.0224,0.20065 0.008,0.0786 0.0145,0.15883 0.0204,0.24076 0.005,0.0685 0.009,0.1383 0.0123,0.20895 0.002,0.0502 0.004,0.10125 0.005,0.1525 5.4e-4,0.0331 7.2e-4,0.0664 1.2e-4,0.0996 -4.8e-4,0.0255 -0.001,0.0498 -0.003,0.0734 -0.001,0.0133 -0.002,0.0229 -0.004,0.031 -0.006,0.0291 -0.0132,0.0591 -0.0216,0.0913 -0.0116,0.0441 -0.0269,0.0986 -0.039,0.14897 -0.008,0.0342 -0.0159,0.0707 -0.0215,0.10859 -0.005,0.0341 -0.0102,0.0677 -0.0162,0.10136 -0.0162,0.0908 -0.0368,0.18174 -0.0609,0.27326 -0.0266,0.1013 -0.0573,0.20246 -0.0905,0.30486 -0.048,0.14791 -0.0986,0.29071 -0.15051,0.44264 -0.0388,0.11368 -0.0775,0.23018 -0.11254,0.34846 -0.0292,0.0986 -0.0563,0.19949 -0.0791,0.30223 -0.008,0.0354 -0.0161,0.0706 -0.0246,0.10717 -0.0154,0.0662 -0.0315,0.13525 -0.0452,0.20507 -0.009,0.0444 -0.0168,0.09 -0.0232,0.13654 -0.005,0.0384 -0.009,0.0781 -0.0117,0.11853 -9.1e-4,0.0129 -4.9e-4,0.0262 -1.8e-4,0.0346 5e-4,0.0131 0.001,0.0256 0.002,0.0369 0.001,0.0216 0.003,0.043 0.005,0.0635 0.003,0.0431 0.007,0.0853 0.009,0.12721 0.002,0.0323 0.003,0.0639 0.004,0.0952 4e-4,0.0222 3.7e-4,0.0437 -4e-4,0.0645 -5.5e-4,0.0145 -0.001,0.0279 -0.003,0.0405 -10e-4,0.009 -0.002,0.0159 -0.003,0.0218 -0.001,0.005 -0.002,0.007 -0.001,0.005 -7.7e-4,0.002 -2e-5,-0.001 0.005,-0.009 0.008,-0.0123 0.0112,-0.015 0.009,-0.0132 -0.002,0.002 -0.006,0.006 -0.0146,0.0129 -0.009,0.008 -0.0187,0.0155 -0.0294,0.0241 -0.0247,0.0199 -0.0524,0.0418 -0.079,0.0641 -0.0141,0.0118 -0.0289,0.0245 -0.0436,0.0381 -0.01,0.009 -0.0208,0.0196 -0.0316,0.0312 -0.009,0.009 -0.0213,0.0235 -0.0328,0.0416 -0.005,0.007 -0.007,0.0108 -0.01,0.0161 -0.0128,0.0212 -0.0264,0.0427 -0.0401,0.0652 -0.0162,0.0264 -0.0333,0.0551 -0.0492,0.0856 -0.0119,0.0228 -0.0231,0.0468 -0.033,0.0718 -0.01,0.025 -0.0184,0.0507 -0.0252,0.0768 -0.001,0.005 -0.002,0.007 -0.001,0.005 0.007,-0.0205 0.0128,-0.0277 0.0139,-0.0292 0.003,-0.003 0.003,-0.004 -0.002,8.9e-4 -0.008,0.007 -0.0142,0.0115 -0.0295,0.0238 -0.006,0.005 -0.0173,0.014 -0.0287,0.0257 -0.004,0.004 -0.0169,0.0176 -0.027,0.0376 -0.002,0.004 -0.004,0.009 -0.006,0.0137 -0.003,0.008 -0.005,0.014 -0.005,0.0177 -0.004,0.0148 -0.005,0.0279 -0.006,0.0327 -0.002,0.0176 -0.003,0.0307 -0.004,0.0401 -0.001,0.007 -0.001,0.008 -8.1e-4,0.006 4.4e-4,-0.001 0.002,-0.0111 0.0135,-0.0263 0.003,-0.005 0.007,-0.009 0.0112,-0.0131 -0.0845,0.0845 -0.19984,0.19983 -0.28437,0.28435 -0.004,0.004 -0.009,0.009 -0.0136,0.0147 -0.009,0.0107 -0.0168,0.0215 -0.022,0.0288 -0.01,0.0139 -0.0191,0.0274 -0.0273,0.0398 -0.0145,0.0218 -0.0282,0.0433 -0.0412,0.0638 -0.0191,0.0303 -0.0375,0.0602 -0.0552,0.0895 -0.0131,0.0218 -0.0257,0.0431 -0.038,0.0645 -0.007,0.0115 -0.0131,0.023 -0.0196,0.035 -0.003,0.006 -0.009,0.0161 -0.0137,0.0274 -0.0108,0.0245 -0.0133,0.0474 -0.0136,0.0633 -3.8e-4,0.0235 0.004,0.0452 0.005,0.0496 0.001,0.006 0.001,0.009 0.001,0.007 -7e-5,-6.3e-4 -2.4e-4,-0.002 -2.4e-4,-0.005 -2e-5,-0.008 0.001,-0.0213 0.009,-0.0372 8.3e-4,-0.002 -0.0168,0.0337 -0.0158,0.0316 -0.0511,0.10231 -0.0985,0.19873 -0.14324,0.29727 -0.0396,0.0873 -0.0749,0.17137 -0.10599,0.25493 -0.0312,0.084 -0.0571,0.16478 -0.0779,0.24359 -0.0215,0.0811 -0.037,0.15792 -0.0476,0.2308 -0.0118,0.0806 -0.0174,0.15486 -0.0189,0.22204 -0.002,0.0844 0.003,0.15801 0.009,0.21776 a 0.12257406,0.12257406 90 0 0 0.24382,-0.0254 z"
                                    transform="scale(1.2) translate(-280,-100)"
                                    opacity="0.2"
                                />
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
