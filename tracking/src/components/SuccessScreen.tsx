"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Star, CheckCircle, FileText, Download, Heart, RefreshCw } from "lucide-react";
import confetti from "canvas-confetti";

interface SuccessScreenProps {
  onReset: () => void;
  trackingId: string;
}

export default function SuccessScreen({ onReset, trackingId }: SuccessScreenProps) {
  const [rating, setRating] = useState<number>(0);
  const [hoveredRating, setHoveredRating] = useState<number>(0);
  const [isDownloading, setIsDownloading] = useState<boolean>(false);
  const [downloadSuccess, setDownloadSuccess] = useState<boolean>(false);
  const [feedbackSent, setFeedbackSent] = useState<boolean>(false);

  // Trigger high-quality confetti celebration bursts
  useEffect(() => {
    // Primary explosion
    confetti({
      particleCount: 120,
      spread: 70,
      origin: { y: 0.5 },
      colors: ["#8b5cf6", "#06b6d4", "#22c55e", "#fbbf24"],
    });

    // Secondary side bursts
    const end = Date.now() + 1.5 * 1000;
    const interval = setInterval(() => {
      if (Date.now() > end) return clearInterval(interval);
      
      confetti({
        particleCount: 30,
        angle: 60,
        spread: 55,
        origin: { x: 0, y: 0.65 },
        colors: ["#8b5cf6", "#06b6d4"],
      });
      confetti({
        particleCount: 30,
        angle: 120,
        spread: 55,
        origin: { x: 1, y: 0.65 },
        colors: ["#22c55e", "#fbbf24"],
      });
    }, 250);

    return () => clearInterval(interval);
  }, []);

  const handleDownloadInvoice = () => {
    if (isDownloading || downloadSuccess) return;
    setIsDownloading(true);
    
    // Simulate premium invoice compilation and file download
    setTimeout(() => {
      setIsDownloading(false);
      setDownloadSuccess(true);
      
      // Auto reset download button checkmark after a few seconds
      setTimeout(() => setDownloadSuccess(false), 3000);
      
      // Trigger browser mock file download
      const element = document.createElement("a");
      const file = new Blob([`FACTION PREMIUM STORE INVOICE\nTracking ID: ${trackingId}\nStatus: Delivered Successfully\nThank you for shopping with Faction.`], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = `Invoice-${trackingId}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }, 2000);
  };

  const handleRatingSubmit = (selected: number) => {
    setRating(selected);
    setFeedbackSent(true);
    // Extra micro-confetti on high ratings
    if (selected >= 4) {
      confetti({
        particleCount: 40,
        spread: 40,
        origin: { y: 0.8 },
      });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="glass-card-bright relative p-8 md:p-10 w-full text-center overflow-hidden border-green-500/20 shadow-[0_0_50px_-10px_rgba(34,197,94,0.15)]"
    >
      {/* Visual Ambient Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 -z-10 w-72 h-72 rounded-full bg-green-500/10 blur-[80px]" />

      {/* Floating Checkmark Icon */}
      <motion.div
        initial={{ scale: 0, rotate: -45 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: "spring", stiffness: 120, damping: 10, delay: 0.2 }}
        className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-green-500/10 border border-green-500/30 shadow-[0_0_30px_rgba(34,197,94,0.3)] active-pulse-green"
      >
        <CheckCircle className="h-10 w-10 text-green-400" />
      </motion.div>

      {/* Heading Text */}
      <motion.h1
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="font-display text-3xl md:text-4xl font-extrabold tracking-tight bg-gradient-to-r from-green-400 via-emerald-400 to-cyan-400 bg-clip-text text-transparent"
      >
        Delivered Successfully
      </motion.h1>

      <motion.p
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="mt-2 text-zinc-400 max-w-md mx-auto text-sm md:text-base font-medium"
      >
        Your parcel has been delivered to your doorstep. Thank you for choosing us!
      </motion.p>

      {/* Separator */}
      <div className="my-8 border-t border-white/5" />

      {/* Main Grid: Rating and Invoice download */}
      <div className="grid md:grid-cols-2 gap-6 max-w-2xl mx-auto items-stretch">
        
        {/* Rating Card */}
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-5 flex flex-col items-center justify-center relative border-white/5 hover:border-purple-500/20 transition-all duration-300"
        >
          <h3 className="text-xs font-semibold uppercase tracking-widest text-purple-400 mb-3 flex items-center gap-1.5">
            <Heart className="h-3.5 w-3.5 fill-current" /> Rate Delivery
          </h3>
          
          <AnimatePresence mode="wait">
            {!feedbackSent ? (
              <motion.div 
                key="rating-stars"
                className="flex items-center gap-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                {[1, 2, 3, 4, 5].map((star) => (
                  <motion.button
                    key={star}
                    type="button"
                    onClick={() => handleRatingSubmit(star)}
                    onMouseEnter={() => setHoveredRating(star)}
                    onMouseLeave={() => setHoveredRating(0)}
                    whileHover={{ scale: 1.25, rotate: 10 }}
                    whileTap={{ scale: 0.9 }}
                    className="p-1 focus:outline-none"
                  >
                    <Star
                      className={`h-7 w-7 transition-all duration-200 ${
                        star <= (hoveredRating || rating)
                          ? "fill-yellow-400 text-yellow-400 filter drop-shadow-[0_0_8px_rgba(250,204,21,0.5)]"
                          : "text-zinc-600 hover:text-zinc-500"
                      }`}
                    />
                  </motion.button>
                ))}
              </motion.div>
            ) : (
              <motion.div 
                key="rating-thanks"
                className="text-center"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 100 }}
              >
                <div className="text-sm text-green-400 font-semibold mb-1">Feedback Received!</div>
                <div className="text-xs text-zinc-400">Thanks for giving us {rating} stars.</div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Invoice Download Card */}
        <motion.div
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-5 flex flex-col items-center justify-center border-white/5 hover:border-cyan-500/20 transition-all duration-300"
        >
          <h3 className="text-xs font-semibold uppercase tracking-widest text-cyan-400 mb-3 flex items-center gap-1.5">
            <FileText className="h-3.5 w-3.5" /> Shipment Details
          </h3>
          
          <motion.button
            onClick={handleDownloadInvoice}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
            className={`w-full py-3 px-4 rounded-xl flex items-center justify-center gap-2 border font-medium text-sm transition-all duration-300 ${
              downloadSuccess 
                ? "bg-green-500/10 border-green-500/30 text-green-400"
                : "bg-white/5 border-white/10 hover:bg-white/10 text-white"
            }`}
          >
            {isDownloading ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin text-cyan-400" />
                <span>Compiling Invoice...</span>
              </>
            ) : downloadSuccess ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-400" />
                <span>Downloaded Invoice!</span>
              </>
            ) : (
              <>
                <Download className="h-4 w-4 text-cyan-400" />
                <span>Download Invoice</span>
              </>
            )}
          </motion.button>
        </motion.div>
      </div>

      {/* Reset/Track another shipment button */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="mt-8"
      >
        <button
          onClick={onReset}
          className="text-xs font-semibold uppercase tracking-widest text-zinc-500 hover:text-zinc-300 hover:glow-text-purple transition-all duration-300 border-b border-transparent hover:border-zinc-500"
        >
          ← Track Another Package
        </button>
      </motion.div>
    </motion.div>
  );
}
