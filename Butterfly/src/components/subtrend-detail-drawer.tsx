import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Subtrend, Startup } from "@/types";
import { fetchStartups } from "@/lib/api";
import { StartupListItem } from "./startup-list-item";
import { LoadingSkeleton } from "./loading-skeleton";
import { MomentumBadge } from "@/components/ui/momentum-badge";
import { SectionHeader } from "./section-header";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { X, ArrowLeft, AlertCircle, TrendingUp, TrendingDown } from "lucide-react";
import { useIsMobile } from "@/hooks/use-mobile";

interface SubtrendDetailDrawerProps {
  subtrend: Subtrend | null;
  isOpen: boolean;
  onClose: () => void;
}

export function SubtrendDetailDrawer({ subtrend, isOpen, onClose }: SubtrendDetailDrawerProps) {
  const [startups, setStartups] = useState<Startup[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isMobile = useIsMobile();

  useEffect(() => {
    if (!isOpen || !subtrend) return;

    const loadStartups = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const data = await fetchStartups(subtrend.id, 3);
        setStartups(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load startups');
        setStartups([]);
      } finally {
        setLoading(false);
      }
    };

    loadStartups();
  }, [isOpen, subtrend]);

  // Handle keyboard events
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!subtrend) return null;

  const content = (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex-shrink-0 p-6 border-b border-border/50">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0 pr-4">
            <h2 className="text-2xl font-bold mb-2 text-foreground">
              {subtrend.name}
            </h2>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {subtrend.description}
            </p>
          </div>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="flex-shrink-0"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
        
        {/* Metrics */}
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <MomentumBadge 
              score={subtrend.momentum_score} 
              change={subtrend.change_30d_pct}
              size="lg" 
            />
            <div className="text-sm text-muted-foreground">
              Current momentum score
            </div>
          </div>
          
          {/* 30-day change indicator */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-muted-foreground">30-day change</span>
            </div>
            <div className="flex items-center gap-3 p-4 glass rounded-lg">
              {subtrend.change_30d_pct > 0 ? (
                <TrendingUp className="w-6 h-6 text-momentum-up" />
              ) : (
                <TrendingDown className="w-6 h-6 text-momentum-down" />
              )}
              <div>
                <div className="text-lg font-semibold">
                  {subtrend.change_30d_pct > 0 ? '+' : ''}{subtrend.change_30d_pct.toFixed(1)}%
                </div>
                <div className="text-xs text-muted-foreground">
                  vs previous 30 days
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <SectionHeader
          title="Top Startups"
          description="These startups ride the wave spotted by Butterfly"
          className="mb-6 text-left"
        />
        
        {loading && (
          <LoadingSkeleton variant="startup" count={3} />
        )}
        
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-3 p-4 glass rounded-lg border border-destructive/20 bg-destructive/5"
          >
            <AlertCircle className="w-5 h-5 text-destructive" />
            <div>
              <p className="text-sm font-medium text-destructive">Failed to load startups</p>
              <p className="text-xs text-destructive/80">{error}</p>
            </div>
          </motion.div>
        )}
        
        {!loading && !error && startups.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="text-muted-foreground mb-2">No startups found</div>
            <div className="text-sm text-muted-foreground/60">
              Check back later for updates
            </div>
          </motion.div>
        )}
        
        {!loading && !error && startups.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            {startups.map((startup, index) => (
              <StartupListItem
                key={startup.id}
                startup={startup}
                index={index}
              />
            ))}
          </motion.div>
        )}
      </div>
      
      {/* Footer */}
      <div className="flex-shrink-0 p-6 border-t border-border/50">
        <Button
          variant="outline"
          onClick={onClose}
          className="w-full"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to subtrends
        </Button>
      </div>
    </div>
  );

  if (isMobile) {
    return (
      <Sheet open={isOpen} onOpenChange={(open) => !open && onClose()}>
        <SheetContent side="bottom" className="h-[90vh] p-0">
          <SheetHeader className="sr-only">
            <SheetTitle>{subtrend.name}</SheetTitle>
          </SheetHeader>
          {content}
        </SheetContent>
      </Sheet>
    );
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50"
            onClick={onClose}
          />
          
          {/* Drawer */}
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 20, stiffness: 300 }}
            className="fixed right-0 top-0 bottom-0 w-full max-w-2xl bg-background border-l border-border z-50"
          >
            {content}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}