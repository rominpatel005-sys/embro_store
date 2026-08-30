"use client";

import React from "react";
import { motion } from "framer-motion";

interface AnimatedTruckProps {
  className?: string;
  isMoving?: boolean;
}

export default function AnimatedTruck({ className = "", isMoving = true }: AnimatedTruckProps) {
  return (
    <div className={`relative flex items-center justify-center ${className}`}>
      {/* Light Trail / Glow Effect Behind Truck */}
      {isMoving && (
        <div className="absolute -left-6 bottom-4 right-1/2 -z-10 h-6 bg-gradient-to-r from-transparent via-cyan-500/10 to-purple-500/30 blur-md rounded-full pointer-events-none" />
      )}

      {/* Exhaust Smoke Particles */}
      {isMoving && (
        <div className="absolute -left-5 bottom-4 flex gap-1 items-end pointer-events-none">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="h-2 w-2 rounded-full bg-zinc-600/40 blur-[1px]"
              animate={{
                x: [-5, -25 - i * 10],
                y: [0, -12 - i * 4],
                scale: [0.6, 1.6],
                opacity: [0.6, 0],
              }}
              transition={{
                duration: 1 + i * 0.2,
                repeat: Infinity,
                delay: i * 0.3,
                ease: "easeOut",
              }}
            />
          ))}
        </div>
      )}

      {/* Truck Body & Chassis Wrapper */}
      <motion.div
        animate={isMoving ? { y: [0, -2, 0] } : {}}
        transition={{
          duration: 0.6,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="relative"
      >
        <svg
          width="110"
          height="65"
          viewBox="0 0 110 65"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="drop-shadow-[0_10px_15px_rgba(0,0,0,0.5)]"
        >
          {/* Headlight Beam (Cyan Glow) */}
          <polygon
            points="102,38 150,25 150,55 102,44"
            fill="url(#headlight-beam)"
            opacity={isMoving ? 0.35 : 0.15}
            className={isMoving ? "animate-headlight-pulse" : ""}
          />

          {/* Definitions for Gradients */}
          <defs>
            {/* Cabin Metallic Gradient */}
            <linearGradient id="cabin-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#c084fc" />
              <stop offset="60%" stopColor="#8b5cf6" />
              <stop offset="100%" stopColor="#6d28d9" />
            </linearGradient>

            {/* Windshield Gradient */}
            <linearGradient id="glass-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#67e8f9" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0e7490" stopOpacity="0.4" />
            </linearGradient>

            {/* Cargo Box Gradient */}
            <linearGradient id="cargo-grad" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#1e1e24" />
              <stop offset="100%" stopColor="#0f0f12" />
            </linearGradient>

            {/* Package (Box) Gradient */}
            <linearGradient id="package-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#fbbf24" />
              <stop offset="100%" stopColor="#b45309" />
            </linearGradient>

            {/* Headlight beam glow */}
            <linearGradient id="headlight-beam" x1="0" y1="0.5" x2="1" y2="0.5">
              <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.8" />
              <stop offset="30%" stopColor="#22d3ee" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#22d3ee" stopOpacity="0" />
            </linearGradient>

            {/* Wheel Spoke Ring */}
            <radialGradient id="wheel-grad" cx="0.5" cy="0.5" r="0.5">
              <stop offset="0%" stopColor="#27272a" />
              <stop offset="85%" stopColor="#09090b" />
              <stop offset="100%" stopColor="#71717a" />
            </radialGradient>
          </defs>

          {/* Under carriage / metal links */}
          <rect x="25" y="44" width="60" height="4" fill="#27272a" rx="2" />

          {/* Main Cargo Container (Premium Dark Matte) */}
          <rect
            x="12"
            y="15"
            width="60"
            height="32"
            rx="4"
            fill="url(#cargo-grad)"
            stroke="rgba(255,255,255,0.08)"
            strokeWidth="1.5"
          />
          {/* Cargo design grooves */}
          <line x1="24" y1="18" x2="24" y2="44" stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
          <line x1="36" y1="18" x2="36" y2="44" stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
          <line x1="48" y1="18" x2="48" y2="44" stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
          <line x1="60" y1="18" x2="60" y2="44" stroke="rgba(255,255,255,0.04)" strokeWidth="1" />

          {/* Bouncing Package in Open Truck Bed (between container and cabin or represented as floating cargo) */}
          {/* Package details */}
          <g>
            <motion.rect
              x="5"
              y="22"
              width="14"
              height="14"
              rx="2"
              fill="url(#package-grad)"
              animate={isMoving ? { y: [22, 20, 22] } : {}}
              transition={{
                duration: 0.5,
                repeat: Infinity,
                delay: 0.1,
                ease: "easeInOut",
              }}
            />
            {/* Box Ribbon */}
            <motion.rect
              x="11"
              y="22"
              width="2"
              height="14"
              fill="#d97706"
              animate={isMoving ? { y: [22, 20, 22] } : {}}
              transition={{
                duration: 0.5,
                repeat: Infinity,
                delay: 0.1,
                ease: "easeInOut",
              }}
            />
          </g>

          {/* Cabin (Purple Glow Metallic Frame) */}
          <path
            d="M72 20H88C93.5 20 98 24.5 98 30V47H72V20Z"
            fill="url(#cabin-grad)"
            stroke="rgba(255,255,255,0.15)"
            strokeWidth="1"
          />

          {/* Cabin Windshield Glass */}
          <path
            d="M84 22H88C91.5 22 94.5 25 94.8 28.5L96.2 35H84V22Z"
            fill="url(#glass-grad)"
          />

          {/* Door Line */}
          <line x1="80" y1="20" x2="80" y2="47" stroke="#4c1d95" strokeWidth="1.5" />
          
          {/* Door Handle (Metallic) */}
          <rect x="82" y="32" width="4" height="2" fill="#e4e4e7" rx="0.5" />

          {/* Headlights (Cyan Glowing Bulbs) */}
          <circle cx="100" cy="40" r="3" fill="#22d3ee" className="glow-shadow-cyan" />
          <circle cx="98" cy="43" r="2" fill="#22d3ee" />

          {/* Front Bumper */}
          <rect x="94" y="47" width="10" height="3" fill="#3f3f46" rx="1.5" />

          {/* Rear Bumper / Guard */}
          <rect x="6" y="45" width="6" height="3" fill="#3f3f46" rx="1" />

          {/* Tail light (Pulsing Red) */}
          <rect x="10" y="38" width="2" height="6" fill="#ef4444" opacity={isMoving ? 0.9 : 0.6} />

          {/* Animated Wheels Group */}
          {/* Wheel 1 (Rear) */}
          <g transform="translate(30, 48)">
            <circle cx="0" cy="0" r="11" fill="url(#wheel-grad)" />
            <circle cx="0" cy="0" r="5" fill="#18181b" stroke="#71717a" strokeWidth="1.5" />
            <g className={isMoving ? "animate-wheel-spin" : ""}>
              {/* Wheel Spokes */}
              <line x1="-8" y1="0" x2="8" y2="0" stroke="#71717a" strokeWidth="1" />
              <line x1="0" y1="-8" x2="0" y2="8" stroke="#71717a" strokeWidth="1" />
              <line x1="-5.6" y1="-5.6" x2="5.6" y2="5.6" stroke="#71717a" strokeWidth="1" />
              <line x1="-5.6" y1="5.6" x2="5.6" y2="-5.6" stroke="#71717a" strokeWidth="1" />
            </g>
          </g>

          {/* Wheel 2 (Front) */}
          <g transform="translate(80, 48)">
            <circle cx="0" cy="0" r="11" fill="url(#wheel-grad)" />
            <circle cx="0" cy="0" r="5" fill="#18181b" stroke="#71717a" strokeWidth="1.5" />
            <g className={isMoving ? "animate-wheel-spin" : ""}>
              {/* Wheel Spokes */}
              <line x1="-8" y1="0" x2="8" y2="0" stroke="#71717a" strokeWidth="1" />
              <line x1="0" y1="-8" x2="0" y2="8" stroke="#71717a" strokeWidth="1" />
              <line x1="-5.6" y1="-5.6" x2="5.6" y2="5.6" stroke="#71717a" strokeWidth="1" />
              <line x1="-5.6" y1="5.6" x2="5.6" y2="-5.6" stroke="#71717a" strokeWidth="1" />
            </g>
          </g>
        </svg>
      </motion.div>

      {/* Under-truck Shadows */}
      <motion.div
        className="absolute bottom-2 left-4 w-20 h-2 bg-black/60 rounded-full blur-[4px]"
        animate={isMoving ? { scaleX: [1, 0.95, 1], opacity: [0.6, 0.45, 0.6] } : {}}
        transition={{
          duration: 0.6,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    </div>
  );
}
