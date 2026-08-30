"use client";

import React from "react";
import { motion } from "framer-motion";
import AnimatedTruck from "./AnimatedTruck";

interface TrackingMapProps {
  currentStep: number; // 0 to 7
  isTransitioning: boolean;
}

interface MapNode {
  name: string;
  x: number;
  y: number;
}

const MAP_NODES: MapNode[] = [
  { name: "Mumbai Terminal", x: 60, y: 220 },
  { name: "Valsad Junction", x: 150, y: 175 },
  { name: "Surat Hub", x: 230, y: 240 },
  { name: "Vadodara Hub", x: 340, y: 180 },
  { name: "Ahmedabad Hub", x: 460, y: 120 },
  { name: "Udaipur Center", x: 590, y: 190 },
  { name: "Jaipur Gateway", x: 740, y: 110 },
  { name: "New Delhi Delivery Hub", x: 890, y: 140 },
];

export default function TrackingMap({ currentStep, isTransitioning }: TrackingMapProps) {
  // Generate the curved path d-attribute linking the nodes
  const pathD = `M 60,220 
                 C 105,190 105,190 150,175 
                 C 195,160 185,270 230,240 
                 C 275,210 295,195 340,180 
                 C 385,165 415,100 460,120 
                 C 505,140 545,225 590,190 
                 C 635,155 695,125 740,110 
                 C 785,95 845,155 890,140`;

  // Get truck's current position on the map based on currentStep
  const activeNode = MAP_NODES[Math.min(currentStep, MAP_NODES.length - 1)];

  return (
    <div className="relative w-full h-[320px] bg-black/45 rounded-3xl border border-white/5 overflow-hidden backdrop-blur-md">
      {/* Background Stylized Topography / Grid */}
      <div className="absolute inset-0 opacity-15 pointer-events-none">
        <svg width="100%" height="100%">
          <defs>
            <pattern id="map-grid" width="30" height="30" patternUnits="userSpaceOnUse">
              <path d="M 30 0 L 0 0 0 30" fill="none" stroke="rgba(255,255,255,0.4)" strokeWidth="0.5" />
            </pattern>
            <radialGradient id="map-glow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.15" />
              <stop offset="100%" stopColor="transparent" stopOpacity="0" />
            </radialGradient>
          </defs>
          <rect width="100%" height="100%" fill="url(#map-grid)" />
          {/* Subtle stylized topographic line layers */}
          <path d="M -50,100 Q 150,200 400,100 T 900,180 T 1200,80" fill="none" stroke="#8b5cf6" strokeWidth="1" opacity="0.3" />
          <path d="M -50,150 Q 200,80 450,220 T 1000,120" fill="none" stroke="#22d3ee" strokeWidth="1" opacity="0.2" />
        </svg>
      </div>

      {/* Map Radial Glow behind the Active Truck */}
      <div 
        className="absolute w-[200px] h-[200px] rounded-full bg-gradient-to-r from-purple-500/10 to-cyan-500/10 blur-3xl pointer-events-none transition-all duration-1000 ease-out-expo"
        style={{
          left: `${activeNode.x - 100}px`,
          top: `${activeNode.y - 100}px`,
        }}
      />

      {/* Main SVG Render Container */}
      <svg className="absolute inset-0 w-full h-full" viewBox="0 0 950 320" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="route-gradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="50%" stopColor="#a855f7" />
            <stop offset="100%" stopColor="#22d3ee" />
          </linearGradient>
          <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Outer glowing trace of the route */}
        <path
          d={pathD}
          fill="none"
          stroke="url(#route-gradient)"
          strokeWidth="6"
          strokeLinecap="round"
          opacity="0.15"
          filter="url(#neon-glow)"
        />

        {/* The core route path */}
        <path
          id="shipment-path"
          d={pathD}
          fill="none"
          stroke="url(#route-gradient)"
          strokeWidth="2.5"
          strokeLinecap="round"
        />

        {/* Dynamic Glowing Dash Particles Flowing along the Route */}
        <path
          d={pathD}
          fill="none"
          stroke="#22d3ee"
          strokeWidth="3.5"
          strokeDasharray="15 150"
          className="animate-road-dash"
          filter="url(#neon-glow)"
        />

        {/* Map Node Connectors and Markers */}
        {MAP_NODES.map((node, index) => {
          const isCompleted = index < currentStep;
          const isActive = index === currentStep;
          return (
            <g key={node.name} className="group">
              {/* Pulsing Active Ring */}
              {isActive && (
                <motion.circle
                  cx={node.x}
                  cy={node.y}
                  r="14"
                  fill="transparent"
                  stroke="#a855f7"
                  strokeWidth="1.5"
                  animate={{ r: [8, 18, 8], opacity: [0.8, 0, 0.8] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                />
              )}

              {/* Node Hotspot Dot */}
              <circle
                cx={node.x}
                cy={node.y}
                r={isActive ? "6" : "4.5"}
                className="transition-all duration-500"
                fill={
                  isCompleted
                    ? "#22c55e"
                    : isActive
                    ? "#a855f7"
                    : "#3f3f46"
                }
                filter={isCompleted || isActive ? "url(#neon-glow)" : ""}
              />

              {/* Hover effect highlight circle */}
              <circle
                cx={node.x}
                cy={node.y}
                r="16"
                fill="transparent"
                className="cursor-pointer hover:fill-white/5 transition-colors duration-200"
              />

              {/* Premium City Labels */}
              <text
                x={node.x}
                y={node.y - 12}
                textAnchor="middle"
                className={`text-[9px] font-medium tracking-wider select-none pointer-events-none transition-all duration-300 font-sans ${
                  isActive
                    ? "fill-purple-400 font-semibold"
                    : isCompleted
                    ? "fill-zinc-400"
                    : "fill-zinc-600"
                }`}
              >
                {node.name}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Floating Animated Truck Layer */}
      <motion.div
        className="absolute z-20 pointer-events-none"
        animate={{
          x: activeNode.x - 55, // Center the truck horizontally
          y: activeNode.y - 48, // Lift truck slightly above coordinate
        }}
        transition={{
          type: "spring",
          stiffness: 45,
          damping: 12,
        }}
      >
        <AnimatedTruck isMoving={isTransitioning} className="scale-65" />
      </motion.div>

      {/* Map Coordinates Floating HUD Badge */}
      <div className="absolute top-4 right-4 flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/5 bg-zinc-950/60 backdrop-blur-md text-[10px] text-zinc-400 font-mono tracking-widest uppercase">
        <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse" />
        RADAR ACTIVE: {activeNode.x.toFixed(0)}°N / {activeNode.y.toFixed(0)}°E
      </div>
    </div>
  );
}
