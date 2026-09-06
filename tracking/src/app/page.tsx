"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Search, 
  ShoppingBag, 
  Package, 
  Truck, 
  Home, 
  Compass, 
  MapPin, 
  UserCheck, 
  CheckCircle, 
  Compass as TransitIcon, 
  Bell, 
  Play, 
  Pause, 
  RotateCcw, 
  ChevronRight, 
  ChevronLeft,
  ChevronRightSquare,
  Lock,
  Phone,
  Sparkles
} from "lucide-react";
import TrackingMap from "../components/TrackingMap";
import SuccessScreen from "../components/SuccessScreen";

interface ShipmentStep {
  title: string;
  location: string;
  date: string;
  time: string;
  details: string;
  icon: React.ComponentType<any>;
}

const SHIPMENT_STEPS: ShipmentStep[] = [
  {
    title: "Order Confirmed",
    location: "Mumbai Main Terminal",
    date: "July 12, 2026",
    time: "10:30 AM",
    details: "Your order has been logged and confirmed by the retail billing server.",
    icon: ShoppingBag,
  },
  {
    title: "Packed",
    location: "Mumbai Warehouse A-3",
    date: "July 12, 2026",
    time: "02:15 PM",
    details: "Item inspected and secured in a recycled premium carbon-neutral box.",
    icon: Package,
  },
  {
    title: "Picked Up",
    location: "Mumbai Cargo Hub",
    date: "July 12, 2026",
    time: "06:00 PM",
    details: "Parcel accepted and scanned into the Faction logistics network.",
    icon: Truck,
  },
  {
    title: "Warehouse Arrival",
    location: "Valsad Junction Hub",
    date: "July 13, 2026",
    time: "03:45 AM",
    details: "Transit sorting completed. Routed northward towards final destination.",
    icon: Home,
  },
  {
    title: "In Transit",
    location: "Vadodara Transit Corridor",
    date: "July 13, 2026",
    time: "11:20 AM",
    details: "Departed sorting gateway on a high-speed electric courier container.",
    icon: Compass,
  },
  {
    title: "Destination City Hub",
    location: "Ahmedabad Main Hub",
    date: "July 13, 2026",
    time: "04:10 PM",
    details: "Received at regional delivery dispatch center for final zone sorting.",
    icon: MapPin,
  },
  {
    title: "Out For Delivery",
    location: "Ahmedabad West Gateway",
    date: "July 13, 2026",
    time: "05:15 PM",
    details: "Assigned to electric cargo van for doorstep delivery. Courier en route.",
    icon: UserCheck,
  },
  {
    title: "Delivered",
    location: "Customer Residence",
    date: "July 13, 2026",
    time: "05:30 PM",
    details: "Package handed over safely. Signature authenticated and logged.",
    icon: CheckCircle,
  },
];

export default function TrackingPage() {
  // Page States
  const [searchState, setSearchState] = useState<"idle" | "searching" | "success">("idle");
  const [trackingNo, setTrackingNo] = useState("");
  const [activeTrackingNo, setActiveTrackingNo] = useState("");
  const [searchLogs, setSearchLogs] = useState("");
  const [currentStep, setCurrentStep] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isAutoPlaying, setIsAutoPlaying] = useState(false);
  const [toastNotification, setToastNotification] = useState<string | null>(null);

  // Magnetic Button Coordinates
  const [btnPos, setBtnPos] = useState({ x: 0, y: 0 });

  // Refs for auto play timers
  const autoplayTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Handle Search Input Submission
  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!trackingNo.trim()) return;

    setSearchState("searching");
    
    // Premium cinematic search logs animation sequence
    const logs = [
      "Securing encrypted channel...",
      "Resolving tracking hashes on satellite beacons...",
      "Quantum beacon routing authenticated...",
      "Retrieving shipping manifest...",
      "Connected! Rendering live coordinates...",
    ];

    logs.forEach((log, index) => {
      setTimeout(() => {
        setSearchLogs(log);
        if (index === logs.length - 1) {
          setTimeout(() => {
            setActiveTrackingNo(trackingNo.toUpperCase());
            setSearchState("success");
            setCurrentStep(0);
            triggerNotification("Shipment detected: Tracking started.");
          }, 600);
        }
      }, (index + 1) * 700);
    });
  };

  // Magnetic button hover logic
  const handleButtonHover = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    setBtnPos({ x: x * 0.35, y: y * 0.35 });
  };

  const handleButtonLeave = () => {
    setBtnPos({ x: 0, y: 0 });
  };

  // Helper: Trigger beautiful temporary notifications
  const triggerNotification = (message: string) => {
    setToastNotification(message);
    setTimeout(() => {
      setToastNotification((prev) => (prev === message ? null : prev));
    }, 4500);
  };

  // Step Controllers
  const handleNextStep = () => {
    if (currentStep >= SHIPMENT_STEPS.length - 1 || isTransitioning) return;
    setIsTransitioning(true);
    setCurrentStep((prev) => prev + 1);
    
    const nextStepInfo = SHIPMENT_STEPS[currentStep + 1];
    triggerNotification(`Update: Package reached ${nextStepInfo.location} (${nextStepInfo.title})`);

    setTimeout(() => {
      setIsTransitioning(false);
    }, 1500);
  };

  const handlePrevStep = () => {
    if (currentStep <= 0 || isTransitioning) return;
    setIsTransitioning(true);
    setCurrentStep((prev) => prev - 1);
    
    const prevStepInfo = SHIPMENT_STEPS[currentStep - 1];
    triggerNotification(`Correction: Status rolled back to ${prevStepInfo.title}`);

    setTimeout(() => {
      setIsTransitioning(false);
    }, 1500);
  };

  // Autoplay Journey Simulator
  useEffect(() => {
    if (isAutoPlaying) {
      if (currentStep >= SHIPMENT_STEPS.length - 1) {
        setIsAutoPlaying(false);
        return;
      }

      autoplayTimerRef.current = setTimeout(() => {
        setIsTransitioning(true);
        setCurrentStep((prev) => {
          const next = prev + 1;
          const nextStepInfo = SHIPMENT_STEPS[next];
          triggerNotification(`Transit update: Switched to ${nextStepInfo.title}`);
          
          if (next === SHIPMENT_STEPS.length - 1) {
            setIsAutoPlaying(false);
          }
          return next;
        });

        setTimeout(() => {
          setIsTransitioning(false);
        }, 1500);
      }, 4200);
    } else {
      if (autoplayTimerRef.current) {
        clearTimeout(autoplayTimerRef.current);
      }
    }

    return () => {
      if (autoplayTimerRef.current) clearTimeout(autoplayTimerRef.current);
    };
  }, [isAutoPlaying, currentStep]);

  const handleReset = () => {
    setIsAutoPlaying(false);
    setIsTransitioning(false);
    setSearchState("idle");
    setTrackingNo("");
    setActiveTrackingNo("");
  };

  // Progress percentage calculation
  const progressPercentage = Math.round((currentStep / (SHIPMENT_STEPS.length - 1)) * 100);

  return (
    <div className="flex-1 bg-aurora-mesh min-h-screen relative overflow-hidden px-4 md:px-8 py-10 flex flex-col items-center justify-start">
      
      {/* Floating Gradient Blurs / Aurora */}
      <motion.div
        animate={{
          x: [0, 80, -40, 0],
          y: [0, -50, 40, 0],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-[-10%] left-[-10%] w-[350px] md:w-[600px] h-[350px] md:h-[600px] rounded-full bg-purple-500/10 blur-[100px] pointer-events-none -z-20"
      />
      <motion.div
        animate={{
          x: [0, -60, 50, 0],
          y: [0, 60, -30, 0],
        }}
        transition={{
          duration: 22,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute bottom-[-10%] right-[-10%] w-[350px] md:w-[650px] h-[350px] md:h-[650px] rounded-full bg-cyan-500/10 blur-[100px] pointer-events-none -z-20"
      />
      <motion.div
        animate={{
          scale: [1, 1.2, 0.9, 1],
          opacity: [0.3, 0.6, 0.3, 0.3],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-[30%] left-[35%] w-[250px] md:w-[450px] h-[250px] md:h-[450px] rounded-full bg-blue-500/10 blur-[120px] pointer-events-none -z-20"
      />

      {/* Floating Particles Backdrop */}
      <div className="absolute inset-0 pointer-events-none -z-10 opacity-40">
        <svg width="100%" height="100%">
          {[...Array(25)].map((_, i) => (
            <motion.circle
              key={i}
              cx={`${10 + Math.random() * 80}%`}
              cy={`${10 + Math.random() * 80}%`}
              r={1 + Math.random() * 2}
              fill="rgba(168, 85, 247, 0.3)"
              animate={{
                y: [0, -40, 0],
                opacity: [0.2, 0.7, 0.2],
              }}
              transition={{
                duration: 6 + Math.random() * 6,
                repeat: Infinity,
                delay: Math.random() * 5,
                ease: "easeInOut",
              }}
            />
          ))}
        </svg>
      </div>

      {/* Main Header / Title HUD */}
      <header className="w-full max-w-6xl flex items-center justify-between mb-10 md:mb-16 z-30">
        <div className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-purple-500 via-blue-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-purple-500/25">
            <span className="font-display font-extrabold text-black text-lg select-none">F</span>
          </div>
          <span className="font-display font-bold text-sm tracking-[0.2em] uppercase bg-gradient-to-r from-zinc-100 to-zinc-400 bg-clip-text text-transparent">
            Faction Express
          </span>
        </div>
        <div className="text-[10px] text-zinc-500 font-mono tracking-widest uppercase border border-white/5 bg-zinc-950/40 rounded-full px-3.5 py-1.5 backdrop-blur-sm">
          SECURE PROTOCOL V1.2
        </div>
      </header>

      {/* Dynamic Main Body Content */}
      <main className="w-full max-w-6xl flex-1 flex flex-col items-center justify-center z-20">
        
        {/* Active Toast Notifications */}
        <AnimatePresence>
          {toastNotification && (
            <motion.div
              initial={{ opacity: 0, y: -40, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              className="fixed top-8 md:top-12 z-50 glass-card px-6 py-4 flex items-center gap-3 border-purple-500/25 shadow-[0_15px_40px_-10px_rgba(168,85,247,0.2)]"
            >
              <div className="h-7 w-7 rounded-full bg-purple-500/10 flex items-center justify-center border border-purple-500/30">
                <Bell className="h-3.5 w-3.5 text-purple-400 animate-bounce" />
              </div>
              <p className="text-xs font-medium text-zinc-200 tracking-wide font-sans">{toastNotification}</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* STATE 1 & 2: IDLE SEARCH STATE */}
        <AnimatePresence mode="wait">
          {searchState === "idle" || searchState === "searching" ? (
            <motion.div
              key="search-container"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
              className="text-center w-full max-w-2xl py-12 md:py-20 flex flex-col items-center"
            >
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-purple-500/15 bg-purple-500/5 mb-6">
                <Sparkles className="h-3.5 w-3.5 text-purple-400" />
                <span className="text-[10px] font-semibold text-purple-300 tracking-widest uppercase">QUANTUM SHIELD ACTIVE</span>
              </div>

              <h1 className="font-display text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-b from-white via-zinc-100 to-zinc-400 bg-clip-text text-transparent">
                Track Your Package
              </h1>
              
              <p className="mt-4 text-zinc-400 max-w-md text-sm sm:text-base leading-relaxed font-sans">
                Track your premium shipment in real-time with state-of-the-art cinematic coordinates and live feedback updates.
              </p>

              {/* Glassmorphic Search Form */}
              <form 
                onSubmit={handleSearchSubmit}
                className="w-full mt-10 md:mt-12 glass-card p-2 border-white/10 flex items-center relative transition-all duration-500 hover:border-purple-500/20 shadow-[0_30px_70px_rgba(0,0,0,0.7)] group"
              >
                <div className="pl-4 flex items-center text-zinc-500 group-hover:text-purple-400 transition-colors duration-300">
                  <Search className="h-5 w-5" />
                </div>
                
                <input
                  type="text"
                  value={trackingNo}
                  onChange={(e) => setTrackingNo(e.target.value)}
                  disabled={searchState === "searching"}
                  placeholder="Enter tracking ID (e.g. FQN-88371-DEL)..."
                  className="w-full bg-transparent border-none py-4 px-4 text-sm md:text-base text-zinc-100 placeholder-zinc-500 focus:outline-none disabled:text-zinc-500 font-sans"
                />

                {/* Magnetic Neon Search Button */}
                <button
                  type="submit"
                  disabled={searchState === "searching" || !trackingNo.trim()}
                  onMouseMove={handleButtonHover}
                  onMouseLeave={handleButtonLeave}
                  style={{
                    transform: `translate(${btnPos.x}px, ${btnPos.y}px)`,
                  }}
                  className={`py-3 px-6 md:px-8 rounded-xl font-display font-bold text-xs uppercase tracking-widest text-black transition-all duration-300 flex items-center gap-2 select-none ${
                    !trackingNo.trim()
                      ? "bg-zinc-700/50 text-zinc-500 cursor-not-allowed border border-white/5"
                      : searchState === "searching"
                      ? "bg-purple-950 border border-purple-500/30 text-purple-400 cursor-wait shadow-[0_0_20px_rgba(168,85,247,0.2)]"
                      : "bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 hover:scale-[1.03] active:scale-[0.98] shadow-[0_0_30px_rgba(168,85,247,0.3)] hover:shadow-[0_0_40px_rgba(6,182,212,0.4)] cursor-pointer"
                  }`}
                >
                  {searchState === "searching" ? (
                    <>
                      <div className="h-3 w-3 rounded-full border border-purple-400 border-t-transparent animate-spin" />
                      <span>Tracking...</span>
                    </>
                  ) : (
                    <span>Initiate Scan</span>
                  )}
                </button>
              </form>

              {/* Simulated Tech Logs Overlay */}
              <AnimatePresence>
                {searchState === "searching" && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="mt-6 text-xs text-purple-400 font-mono tracking-widest uppercase flex items-center gap-2"
                  >
                    <span className="h-1.5 w-1.5 rounded-full bg-purple-500 animate-ping" />
                    <span>{searchLogs}</span>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ) : (
            
            /* STATE 3: SHIPMENT TRACKING CONSOLE BOARD */
            <motion.div
              key="tracking-container"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, y: 30 }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className="w-full flex flex-col gap-6 md:gap-8 pb-12"
            >
              
              {/* TOP HEADER: Status Title Card */}
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 glass-card p-6 border-white/5">
                <div>
                  <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.25em] font-sans">CURRENT SHIPMENT</span>
                  <div className="flex items-center gap-3 mt-1.5">
                    <h2 className="font-display text-xl md:text-2xl font-extrabold text-white">
                      {activeTrackingNo}
                    </h2>
                    <span className="h-2 w-2 rounded-full bg-green-500 active-pulse-green" />
                    <span className="text-xs text-green-400 font-semibold tracking-wider">Active Stream</span>
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-3">
                  <div className="px-4 py-2 rounded-2xl bg-zinc-950 border border-white/5 text-center min-w-[90px]">
                    <div className="text-[9px] text-zinc-500 uppercase font-semibold">ETA</div>
                    <div className="text-xs text-zinc-300 font-semibold mt-0.5">July 13, 05:30 PM</div>
                  </div>
                  <div className="px-4 py-2 rounded-2xl bg-zinc-950 border border-white/5 text-center min-w-[90px]">
                    <div className="text-[9px] text-zinc-500 uppercase font-semibold">DISTANCE</div>
                    <div className="text-xs text-cyan-400 font-semibold mt-0.5">
                      {currentStep >= 7 ? "0 km" : `${(7 - currentStep) * 45} km`}
                    </div>
                  </div>
                  <button 
                    onClick={handleReset}
                    className="h-10 px-4 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 text-xs font-semibold text-zinc-300 hover:text-white transition-all duration-300 uppercase tracking-widest flex items-center gap-1.5"
                  >
                    <RotateCcw className="h-3.5 w-3.5" /> Close
                  </button>
                </div>
              </div>

              {/* SUCCESS OVERLAY TRIGGER */}
              <AnimatePresence mode="wait">
                {currentStep === 7 && !isTransitioning ? (
                  <SuccessScreen key="success" trackingId={activeTrackingNo} onReset={handleReset} />
                ) : (
                  
                  /* STANDARD CONSOLE BOARD LAYOUT */
                  <motion.div
                    key="standard-layout"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="grid lg:grid-cols-3 gap-6 md:gap-8 items-start"
                  >
                    
                    {/* LEFT & CENTER: Map & Road Visualizers */}
                    <div className="lg:col-span-2 flex flex-col gap-6 md:gap-8">
                      
                      {/* Premium Dark Interactive Map */}
                      <TrackingMap currentStep={currentStep} isTransitioning={isTransitioning} />

                      {/* Timeline Road Checkpoints Dashboard */}
                      <div className="glass-card p-6 md:p-8 border-white/5 flex flex-col gap-6 relative">
                        <div className="flex items-center justify-between">
                          <h3 className="text-xs font-bold uppercase text-zinc-400 tracking-[0.25em] font-sans">Journey Checkpoints</h3>
                          <div className="text-xs font-semibold text-purple-400 bg-purple-500/10 border border-purple-500/15 rounded-full px-3 py-1">
                            {progressPercentage}% Complete
                          </div>
                        </div>

                        {/* Custom Curved Road / Linear Timeline Progress */}
                        {/* We display a premium progress bar with shifting gradient lights */}
                        <div className="w-full relative py-3 bg-zinc-950/60 rounded-2xl border border-white/5 px-6 overflow-hidden flex flex-col justify-center">
                          {/* Shifting Light Bar Background */}
                          <div className="w-full h-2.5 bg-zinc-800/50 rounded-full relative overflow-hidden">
                            <motion.div
                              className="h-full bg-gradient-to-r from-purple-500 via-blue-500 to-cyan-400 rounded-full"
                              animate={{ width: `${progressPercentage}%` }}
                              transition={{ duration: 1, ease: "easeOut" }}
                            />
                            {/* Running Light Streak */}
                            {progressPercentage > 0 && (
                              <motion.div
                                className="absolute top-0 h-full w-[80px] bg-gradient-to-r from-transparent via-white/40 to-transparent"
                                animate={{
                                  left: ["-80px", "100%"],
                                }}
                                transition={{
                                  duration: 2.2,
                                  repeat: Infinity,
                                  ease: "linear",
                                }}
                              />
                            )}
                          </div>
                          
                          <div className="flex justify-between mt-2 font-mono text-[9px] text-zinc-500">
                            <span>MUMBAI ORIGIN</span>
                            <span>TRANSIT HUB</span>
                            <span>DELIVERY POINT</span>
                          </div>
                        </div>

                        {/* Interactive Timeline Checkpoint Glass Cards */}
                        {/* On Desktop: Grid columns. On Mobile: Scrollable Vertical Stack */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                          {SHIPMENT_STEPS.map((step, idx) => {
                            const isCompleted = idx < currentStep;
                            const isActive = idx === currentStep;
                            const isFuture = idx > currentStep;
                            const IconComponent = step.icon;

                            return (
                              <motion.div
                                key={step.title}
                                className={`glass-card p-4 flex flex-col items-start text-left relative transition-all duration-300 overflow-hidden ${
                                  isActive
                                    ? "border-purple-500/40 glow-shadow-purple bg-purple-500/5"
                                    : isCompleted
                                    ? "border-green-500/20 bg-green-950/5"
                                    : "opacity-40 border-white/5"
                                }`}
                                whileHover={!isFuture ? { scale: 1.02, y: -2 } : {}}
                              >
                                {/* Circle Icon Indicator */}
                                <div className="flex items-center justify-between w-full mb-3">
                                  <div
                                    className={`h-9 w-9 rounded-xl flex items-center justify-center border transition-all duration-300 ${
                                      isCompleted
                                        ? "bg-green-500/10 border-green-500/30 text-green-400 shadow-[0_0_15px_rgba(34,197,94,0.2)]"
                                        : isActive
                                        ? "bg-purple-500/10 border-purple-500/40 text-purple-400 active-pulse-purple"
                                        : "bg-zinc-900 border-white/5 text-zinc-600"
                                    }`}
                                  >
                                    <IconComponent className="h-4.5 w-4.5" />
                                  </div>
                                  
                                  {/* Top right checkpoint status tag */}
                                  {isCompleted && (
                                    <span className="text-[8px] font-bold text-green-400 uppercase tracking-wider">OK</span>
                                  )}
                                  {isActive && (
                                    <span className="h-2 w-2 rounded-full bg-purple-400 animate-ping" />
                                  )}
                                </div>

                                {/* Step Metadata */}
                                <h4 className={`text-xs font-bold leading-tight font-display ${isActive ? "text-purple-300" : "text-zinc-200"}`}>
                                  {step.title}
                                </h4>
                                <p className="text-[10px] text-zinc-500 font-medium mt-1 font-sans line-clamp-1">
                                  {step.location}
                                </p>
                                
                                {isActive && (
                                  <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-purple-500 to-cyan-400" />
                                )}
                              </motion.div>
                            );
                          })}
                        </div>

                      </div>
                    </div>

                    {/* RIGHT: Live Location details & Status telemetry controls */}
                    <div className="flex flex-col gap-6 md:gap-8">
                      
                      {/* Glass Info Card: Live Location telemetry */}
                      <div className="glass-card p-6 border-white/5 relative overflow-hidden">
                        {/* Subtle glow background */}
                        <div className="absolute top-[-20%] right-[-20%] w-32 h-32 rounded-full bg-purple-500/5 blur-2xl pointer-events-none" />

                        <h3 className="text-xs font-bold uppercase text-zinc-400 tracking-[0.25em] mb-4 flex items-center justify-between">
                          <span>Live Telemetry</span>
                          <span className="flex items-center gap-1.5 text-[9px] text-green-400 lowercase tracking-normal">
                            <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse" /> ping: 12ms
                          </span>
                        </h3>

                        {/* Location Details Stack */}
                        <div className="flex flex-col gap-4">
                          
                          <div className="bg-zinc-950/50 rounded-2xl border border-white/5 p-4">
                            <label className="text-[9px] font-bold text-zinc-500 uppercase tracking-widest block">Current Node</label>
                            <span className="text-sm font-semibold text-zinc-200 mt-1 block">
                              {SHIPMENT_STEPS[currentStep].location}
                            </span>
                            <span className="text-[10px] text-zinc-400 mt-1 block leading-relaxed italic">
                              "{SHIPMENT_STEPS[currentStep].details}"
                            </span>
                          </div>

                          <div className="grid grid-cols-2 gap-3">
                            <div className="bg-zinc-950/50 rounded-2xl border border-white/5 p-3">
                              <label className="text-[8px] font-bold text-zinc-500 uppercase tracking-widest block">Scan Time</label>
                              <span className="text-xs font-semibold text-zinc-200 mt-0.5 block">
                                {SHIPMENT_STEPS[currentStep].time}
                              </span>
                            </div>
                            <div className="bg-zinc-950/50 rounded-2xl border border-white/5 p-3">
                              <label className="text-[8px] font-bold text-zinc-500 uppercase tracking-widest block">Scan Date</label>
                              <span className="text-xs font-semibold text-zinc-200 mt-0.5 block">
                                {SHIPMENT_STEPS[currentStep].date}
                              </span>
                            </div>
                          </div>

                          {/* Courier Dispatch HUD details */}
                          <div className="bg-zinc-950/50 rounded-2xl border border-white/5 p-4 flex flex-col gap-3">
                            <div className="flex items-center gap-3">
                              <div className="h-10 w-10 rounded-full bg-zinc-900 border border-white/5 flex items-center justify-center">
                                <Truck className="h-4.5 w-4.5 text-zinc-400" />
                              </div>
                              <div>
                                <h5 className="text-xs font-bold text-zinc-300">Courier Driver</h5>
                                <p className="text-[10px] text-zinc-500">Vikram R. (Express Team)</p>
                              </div>
                            </div>
                            <a 
                              href="tel:+919898799182"
                              className="w-full py-2.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-300 hover:bg-purple-500/20 transition-all duration-300 text-center text-xs font-bold flex items-center justify-center gap-1.5 select-none"
                            >
                              <Phone className="h-3.5 w-3.5" /> Call Courier Coordinate
                            </a>
                          </div>

                        </div>
                      </div>

                      {/* MISSION CONTROLLER HUD PANEL */}
                      {/* Glass card displaying playback simulator triggers */}
                      <div className="glass-card p-6 border-white/5 bg-gradient-to-b from-zinc-900/40 to-black/80 relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-12 h-12 bg-purple-500/5 blur-xl pointer-events-none" />

                        <h3 className="text-xs font-bold uppercase text-purple-400 tracking-[0.25em] mb-4 flex items-center gap-1">
                          <Lock className="h-3.5 w-3.5" /> Simulation Console
                        </h3>
                        <p className="text-[10px] text-zinc-500 leading-normal mb-5 font-sans">
                          Manually push step increments, run automated shipment progress flow, or test success modal layouts in real-time.
                        </p>

                        <div className="flex flex-col gap-3">
                          {/* Next / Prev triggers */}
                          <div className="grid grid-cols-2 gap-3">
                            <button
                              onClick={handlePrevStep}
                              disabled={currentStep <= 0 || isTransitioning}
                              className="h-11 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 disabled:opacity-30 text-xs font-bold uppercase tracking-widest text-zinc-300 flex items-center justify-center gap-1 select-none transition-all duration-300"
                            >
                              <ChevronLeft className="h-4 w-4" /> Back
                            </button>
                            <button
                              onClick={handleNextStep}
                              disabled={currentStep >= 7 || isTransitioning}
                              className="h-11 rounded-xl bg-purple-500/15 border border-purple-500/30 hover:bg-purple-500/25 disabled:opacity-30 text-xs font-bold uppercase tracking-widest text-purple-300 flex items-center justify-center gap-1 select-none transition-all duration-300"
                            >
                              Forward <ChevronRight className="h-4 w-4" />
                            </button>
                          </div>

                          {/* Autoplay toggle */}
                          <button
                            onClick={() => setIsAutoPlaying(!isAutoPlaying)}
                            disabled={currentStep >= 7}
                            className={`h-12 w-full rounded-xl border text-xs font-display font-extrabold uppercase tracking-widest select-none flex items-center justify-center gap-2 transition-all duration-300 ${
                              isAutoPlaying
                                ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-300 glow-shadow-cyan"
                                : "bg-gradient-to-r from-purple-500 to-cyan-500 text-white border-transparent hover:scale-[1.02]"
                            }`}
                          >
                            {isAutoPlaying ? (
                              <>
                                <Pause className="h-4 w-4 fill-current" />
                                <span>Pause Autoplay</span>
                              </>
                            ) : (
                              <>
                                <Play className="h-4 w-4 fill-current" />
                                <span>Autoplay Journey</span>
                              </>
                            )}
                          </button>

                          {/* Instant Delivery skip */}
                          <button
                            onClick={() => {
                              setIsAutoPlaying(false);
                              setIsTransitioning(false);
                              setCurrentStep(7);
                              triggerNotification("Simulation skip: Shipment delivered.");
                            }}
                            disabled={currentStep === 7}
                            className="w-full text-center text-[10px] py-1 text-zinc-600 hover:text-zinc-400 select-none uppercase tracking-wider font-semibold"
                          >
                            Skip directly to Delivery success
                          </button>
                        </div>
                      </div>

                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

            </motion.div>
          )}
        </AnimatePresence>

      </main>

      {/* Footer copyright */}
      <footer className="w-full max-w-6xl mt-auto pt-10 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-4 z-20">
        <p className="text-[10px] text-zinc-600 font-mono tracking-wider">
          © 2026 FACTION PREMIUM STORE. ALL RIGHTS RESERVED.
        </p>
        <div className="flex gap-4 text-[10px] text-zinc-600 font-mono tracking-wider">
          <a href="#" className="hover:text-purple-400 transition-colors duration-200">PRIVACY</a>
          <span>/</span>
          <a href="#" className="hover:text-purple-400 transition-colors duration-200">TERMS OF SERVICE</a>
        </div>
      </footer>
    </div>
  );
}
