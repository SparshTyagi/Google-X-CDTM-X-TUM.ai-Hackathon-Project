import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface LoadingSkeletonProps {
  variant?: 'trend' | 'subtrend' | 'startup';
  count?: number;
  className?: string;
}

export function LoadingSkeleton({ variant = 'trend', count = 3, className }: LoadingSkeletonProps) {
  const skeletons = Array.from({ length: count }, (_, i) => i);

  if (variant === 'trend') {
    return (
      <div className={cn("grid grid-cols-1 md:grid-cols-3 gap-6", className)}>
        {skeletons.map((index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="glass p-6 h-80">
              <div className="animate-pulse space-y-4">
                {/* Header */}
                <div className="flex justify-between items-start">
                  <div className="space-y-2">
                    <div className="h-4 bg-muted/30 rounded w-32" />
                    <div className="h-3 bg-muted/20 rounded w-24" />
                  </div>
                  <div className="h-6 bg-muted/30 rounded-full w-8" />
                </div>
                
                {/* Description */}
                <div className="space-y-2">
                  <div className="h-3 bg-muted/20 rounded w-full" />
                  <div className="h-3 bg-muted/20 rounded w-3/4" />
                  <div className="h-3 bg-muted/20 rounded w-1/2" />
                </div>
                
                {/* Progress bar */}
                <div className="mt-auto space-y-2">
                  <div className="h-2 bg-muted/30 rounded-full w-full" />
                  <div className="flex justify-between">
                    <div className="h-6 bg-muted/30 rounded-full w-16" />
                    <div className="h-4 bg-muted/20 rounded w-20" />
                  </div>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    );
  }

  if (variant === 'subtrend') {
    return (
      <div className={cn("grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4", className)}>
        {skeletons.map((index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
          >
            <Card className="glass p-4 h-32">
              <div className="animate-pulse space-y-3 h-full">
                {/* Header */}
                <div className="flex justify-between items-start">
                  <div className="space-y-2 flex-1">
                    <div className="h-3 bg-muted/30 rounded w-3/4" />
                    <div className="h-2 bg-muted/20 rounded w-full" />
                    <div className="h-2 bg-muted/20 rounded w-2/3" />
                  </div>
                  <div className="h-5 bg-muted/30 rounded-full w-12" />
                </div>
                
                {/* Sparkline area */}
                <div className="mt-auto">
                  <div className="h-6 bg-muted/20 rounded w-full" />
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    );
  }

  if (variant === 'startup') {
    return (
      <div className={cn("space-y-4", className)}>
        {skeletons.map((index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass p-4 rounded-lg"
          >
            <div className="animate-pulse flex gap-4">
              {/* Avatar */}
              <div className="w-12 h-12 bg-muted/30 rounded-lg flex-shrink-0" />
              
              {/* Content */}
              <div className="flex-1 space-y-2">
                <div className="flex justify-between items-start">
                  <div className="h-4 bg-muted/30 rounded w-32" />
                  <div className="h-6 bg-muted/20 rounded w-6" />
                </div>
                <div className="space-y-1">
                  <div className="h-3 bg-muted/20 rounded w-full" />
                  <div className="h-3 bg-muted/20 rounded w-3/4" />
                </div>
                <div className="flex gap-2">
                  <div className="h-5 bg-muted/20 rounded-full w-16" />
                  <div className="h-5 bg-muted/20 rounded-full w-12" />
                  <div className="h-5 bg-muted/20 rounded-full w-20" />
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  }

  return null;
}