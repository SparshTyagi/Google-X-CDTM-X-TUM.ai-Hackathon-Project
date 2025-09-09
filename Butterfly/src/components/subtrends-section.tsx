import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Subtrend } from "@/types";
import { getSubtrends } from "@/lib/api";
import { SubtrendTile } from "./subtrend-tile";
import { LoadingSkeleton } from "./loading-skeleton";
import { SectionHeader } from "./section-header";
import { Button } from "@/components/ui/button";
import { AlertCircle, RefreshCw, Filter } from "lucide-react";

interface SubtrendsSectionProps {
  selectedTrendId: string | null;
  onSubtrendClick: (subtrend: Subtrend) => void;
}

export function SubtrendsSection({ selectedTrendId, onSubtrendClick }: SubtrendsSectionProps) {
  const [subtrends, setSubtrends] = useState<Subtrend[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<'momentum' | 'name'>('momentum');

  const loadSubtrends = async (trendId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getSubtrends(trendId);
      setSubtrends(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load subtrends');
      setSubtrends([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedTrendId) {
      loadSubtrends(selectedTrendId);
    }
  }, [selectedTrendId]);

  // Sort subtrends
  const sortedSubtrends = [...subtrends].sort((a, b) => {
    if (sortBy === 'momentum') {
      return b.momentum_score - a.momentum_score;
    }
    return a.name.localeCompare(b.name);
  });

  if (!selectedTrendId) {
    return (
      <section id="subtrends-section" className="py-20 px-4">
        <div className="container mx-auto max-w-7xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-muted-foreground"
          >
            Select a trend above to explore its subtrends
          </motion.div>
        </div>
      </section>
    );
  }

  return (
    <section id="subtrends-section" className="py-20 px-4 relative">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-surface/20 to-transparent" />
      
      <div className="container mx-auto max-w-7xl relative z-10">
        <SectionHeader
          eyebrow="Spotted early by Butterfly"
          title="Explore In-Depth Subtrends"
          description="Subsectors with the highest momentum — reliable signals for smart investors"
          tooltip="Subtrends are ranked by momentum score, calculated from startup activity, funding, and market signals"
          className="mb-12"
        >
          {/* Controls */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex items-center justify-center gap-4 mt-8"
          >
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Sort by:</span>
            </div>
            
            <div className="flex bg-muted/30 rounded-lg p-1">
              <Button
                variant={sortBy === 'momentum' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setSortBy('momentum')}
                className="h-8 px-3"
              >
                Momentum
              </Button>
              <Button
                variant={sortBy === 'name' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setSortBy('name')}
                className="h-8 px-3"
              >
                Name
              </Button>
            </div>
          </motion.div>
        </SectionHeader>

        {/* Content */}
        {loading && (
          <LoadingSkeleton variant="subtrend" count={8} />
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
                <p className="font-medium text-destructive mb-1">Failed to load subtrends</p>
                <p className="text-sm text-destructive/80">{error}</p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => selectedTrendId && loadSubtrends(selectedTrendId)}
                className="ml-4"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Retry
              </Button>
            </div>
          </motion.div>
        )}

        {!loading && !error && subtrends.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-20"
          >
            <div className="text-muted-foreground mb-2">No subtrends available</div>
            <div className="text-sm text-muted-foreground/60">
              This trend may not have detailed subtrend data yet
            </div>
          </motion.div>
        )}

        {!loading && !error && sortedSubtrends.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
          >
            {sortedSubtrends.map((subtrend, index) => (
              <SubtrendTile
                key={subtrend.id}
                subtrend={subtrend}
                index={index}
                onClick={() => onSubtrendClick(subtrend)}
              />
            ))}
          </motion.div>
        )}

        {/* Stats */}
        {!loading && !error && sortedSubtrends.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="text-center mt-12 pt-8 border-t border-border/50"
          >
            <div className="text-sm text-muted-foreground">
              Showing <span className="font-medium text-foreground">{sortedSubtrends.length}</span> subtrends
              {sortBy === 'momentum' && (
                <span className="ml-2">sorted by momentum score</span>
              )}
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
}