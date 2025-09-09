import { motion } from "framer-motion";
import { Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import butterflyLogo from "@/assets/butterfly-logo.svg";

interface ButterflyHeaderProps {
  onSettingsClick?: () => void;
  className?: string;
}

/**
 * Butterfly Header - Premium brand header with logo and tagline
 * "Catch the breeze before it turns into a hurricane."
 */
export function ButterflyHeader({ onSettingsClick, className }: ButterflyHeaderProps) {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className={cn(
        "relative z-50 w-full border-b border-border/50 backdrop-blur-md sticky top-0",
        "bg-gradient-to-r from-background/95 via-background/90 to-background/95",
        className
      )}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo & Brand */}
          <div className="flex items-center gap-4">
            {/* Butterfly Logo */}
            <motion.img
              src={butterflyLogo}
              alt="Butterfly logo - a gradient butterfly symbolizing catching market trends early"
              className="w-10 h-10 drop-shadow-lg"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
            />
            
            <div className="flex flex-col">
              <h1 className="text-xl font-bold tracking-tight text-foreground">
                Butterfly
              </h1>
              <p className="text-sm text-muted-foreground leading-tight max-w-xs sm:max-w-none">
                Catch the breeze before it turns into a hurricane.
              </p>
            </div>
          </div>

          {/* Settings */}
          {onSettingsClick && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onSettingsClick}
              className="text-muted-foreground hover:text-foreground"
              aria-label="Open settings"
            >
              <Settings className="w-5 h-5" />
            </Button>
          )}
        </div>
      </div>

      {/* Subtle bottom glow */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-signature-teal/50 to-transparent" />
    </motion.header>
  );
}