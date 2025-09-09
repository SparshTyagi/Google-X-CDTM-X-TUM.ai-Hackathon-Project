import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Trend } from "@/types";
import { getTrends } from "@/lib/api";
import { TrendCard } from "./trend-card";
import { LoadingSkeleton } from "./loading-skeleton";
import { Button } from "@/components/ui/button";
import { ChevronDown, AlertCircle, RefreshCw } from "lucide-react";

interface HeroSectionProps {
  onExploreClick: (trendId: string) => void;
}

export function HeroSection({ onExploreClick }: HeroSectionProps) {
  const [trends, setTrends] = useState<Trend[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTrends = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getTrends(3);
      setTrends(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load trends');
      setTrends([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTrends();
  }, []);

  const scrollToSubtrends = () => {
    const subtrendsSection = document.getElementById('subtrends-section');
    if (subtrendsSection) {
      subtrendsSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="min-h-screen flex flex-col relative overflow-hidden pt-20">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-signature-teal/5 via-transparent to-primary/5" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-signature-teal/10 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
      
      {/* Content */}
      <div className="relative z-10 flex-1 flex flex-col justify-center px-4 py-20">
        <div className="container mx-auto max-w-7xl">
          {/* Hero Title */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-to-r from-foreground via-signature-teal to-primary bg-clip-text text-transparent">
                Top 3 Trends
              </span>
              <br />
              <span className="text-foreground/80">Right Now</span>
            </h1>
            
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              The highest momentum technologies and markets. 
              Insights VCs can rely on from startup activity, investment flows, and innovation signals.
            </p>
          </motion.div>

          {/* Trends Grid */}
          {loading && (
            <LoadingSkeleton variant="trend" count={3} />
          )}

          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center"
            >
              <div className="inline-flex items-center gap-3 p-6 glass rounded-lg border border-destructive/20 bg-destructive/5">
                <AlertCircle className="w-6 h-6 text-destructive" />
                <div className="text-left">
                  <p className="font-medium text-destructive mb-1">Failed to load trends</p>
                  <p className="text-sm text-destructive/80">{error}</p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={loadTrends}
                  className="ml-4"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Retry
                </Button>
              </div>
            </motion.div>
          )}

          {!loading && !error && trends.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-20"
            >
              <div className="text-muted-foreground mb-2">No trends available</div>
              <div className="text-sm text-muted-foreground/60">
                Check back later for updates
              </div>
            </motion.div>
          )}

          {!loading && !error && trends.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 mb-16">
              {trends.map((trend, index) => (
                <motion.div
                  key={trend.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.2, duration: 0.6 }}
                  className={`
                    ${index === 0 ? 'md:scale-110 md:z-10 relative' : ''}
                    ${index === 1 ? 'md:scale-105' : ''}
                    ${index === 2 ? 'md:scale-100' : ''}
                  `}
                >
                  <TrendCard
                    trend={trend}
                    rank={index + 1}
                    onClick={() => onExploreClick(trend.id)}
                  />
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Scroll indicator */}
      {!loading && !error && trends.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          className="relative z-10 text-center pb-8"
        >
          <Button
            variant="ghost"
            onClick={scrollToSubtrends}
            className="group hover:bg-transparent"
          >
            <div className="flex flex-col items-center gap-2">
              <span className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
                Explore subtrends
              </span>
              <motion.div
                animate={{ y: [0, 4, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <ChevronDown className="w-5 h-5 text-primary" />
              </motion.div>
            </div>
          </Button>
        </motion.div>
      )}
    </section>
  );
}