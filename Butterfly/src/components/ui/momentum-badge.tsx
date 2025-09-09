import { cn } from "@/lib/utils";
import { MomentumBadgeProps } from "@/types";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

export function MomentumBadge({ score, change, size = 'md' }: MomentumBadgeProps) {
  const getVariant = () => {
    if (change !== undefined) {
      if (change > 0) return 'up';
      if (change < 0) return 'down';
    }
    if (score >= 80) return 'up';
    if (score <= 40) return 'down';
    return 'neutral';
  };

  const variant = getVariant();
  
  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5', 
    lg: 'text-base px-4 py-2'
  };

  const iconSize = {
    sm: 12,
    md: 14,
    lg: 16
  };

  const getIcon = () => {
    switch (variant) {
      case 'up':
        return <TrendingUp size={iconSize[size]} />;
      case 'down':
        return <TrendingDown size={iconSize[size]} />;
      default:
        return <Minus size={iconSize[size]} />;
    }
  };

  const formatChange = (value: number) => {
    const sign = value > 0 ? '+' : '';
    return `${sign}${value.toFixed(1)}%`;
  };

  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full font-medium transition-colors",
        sizeClasses[size],
        {
          'momentum-up bg-momentum-up/10 border border-momentum-up/20': variant === 'up',
          'momentum-down bg-momentum-down/10 border border-momentum-down/20': variant === 'down',  
          'momentum-neutral bg-momentum-neutral/10 border border-momentum-neutral/20': variant === 'neutral',
        }
      )}
    >
      {getIcon()}
      <span className="font-mono">
        {score}
        {change !== undefined && (
          <span className="ml-1 opacity-80">
            {formatChange(change)}
          </span>
        )}
      </span>
    </div>
  );
}