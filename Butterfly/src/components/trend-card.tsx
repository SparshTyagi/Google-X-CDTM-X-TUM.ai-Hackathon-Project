import { motion } from "framer-motion";
import { Trend } from "@/types";
import { MomentumBadge } from "@/components/ui/momentum-badge";
import { Card } from "@/components/ui/card";
import { Sparkles, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface TrendCardProps {
  trend: Trend;
  rank: number;
  onClick?: () => void;
  className?: string;
}

export function TrendCard({ trend, rank, onClick, className }: TrendCardProps) {
  const isTopTrend = rank === 1;
  
  // Rank-based styling for clear hierarchy
  const getRankClasses = () => {
    switch (rank) {
      case 1: return "rank-1 premium-sparkle";
      case 2: return "rank-2"; 
      case 3: return "rank-3";
      default: return "";
    }
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: rank * 0.1, duration: 0.5 }}
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={cn("cursor-pointer group", className)}
      onClick={onClick}
    >
      <Card className="glass parallax-hover relative overflow-hidden p-6 h-full">
        {/* Background gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5 opacity-60" />
        
        {/* Rank indicator */}
        <div className="absolute top-4 right-4 flex items-center gap-2">
          {isTopTrend && (
            <Sparkles className="w-4 h-4 text-momentum-up sparkle" />
          )}
          <div className="text-xs font-mono text-muted-foreground bg-muted/50 px-2 py-1 rounded-full">
            #{rank}
          </div>
        </div>
        
        {/* Content */}
        <div className="relative z-10 h-full flex flex-col">
          {/* Header */}
          <div className="mb-4">
            <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
              {trend.name}
            </h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {trend.summary}
            </p>
          </div>
          
          {/* Metrics */}
          <div className="mt-auto space-y-4">
            {/* Momentum meter */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Momentum Score</span>
                <span className="font-mono font-medium">{trend.momentum_score}</span>
              </div>
              
              {/* Animated progress bar */}
              <div className="relative h-2 bg-muted/30 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${trend.momentum_score}%` }}
                  transition={{ delay: rank * 0.1 + 0.3, duration: 0.8, ease: "easeOut" }}
                  className={cn(
                    "h-full rounded-full relative",
                    trend.change_30d_pct > 0 
                      ? "bg-gradient-momentum-up" 
                      : "bg-gradient-momentum-down"
                  )}
                >
                  {/* Glow effect for high scores */}
                  {trend.momentum_score > 80 && (
                    <div className="absolute inset-0 bg-white/20 blur-sm rounded-full" />
                  )}
                </motion.div>
              </div>
            </div>
            
            {/* Badges */}
            <div className="flex items-center justify-between">
              <MomentumBadge 
                score={trend.momentum_score} 
                change={trend.change_30d_pct}
                size="sm"
              />
              
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <TrendingUp className="w-3 h-3" />
                <span>30d change</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Hover effects */}
        <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
        <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 via-accent/20 to-primary/20 rounded-lg opacity-0 group-hover:opacity-100 blur transition-opacity pointer-events-none" />
      </Card>
    </motion.div>
  );
}