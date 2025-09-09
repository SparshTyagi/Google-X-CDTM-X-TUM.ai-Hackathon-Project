import { motion } from "framer-motion";
import { ReactNode } from "react";
import { HelpCircle } from "lucide-react";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  tooltip?: string;
  children?: ReactNode;
  className?: string;
}

export function SectionHeader({ 
  eyebrow, 
  title, 
  description, 
  tooltip, 
  children, 
  className 
}: SectionHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={cn("text-center space-y-4", className)}
    >
      {/* Eyebrow */}
      {eyebrow && (
        <div className="flex items-center justify-center gap-2">
          <div className="h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent w-8" />
          <span className="text-xs uppercase tracking-wider text-primary/80 font-medium">
            {eyebrow}
          </span>
          <div className="h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent w-8" />
        </div>
      )}
      
      {/* Title */}
      <div className="flex items-center justify-center gap-2">
        <h2 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
          {title}
        </h2>
        
        {/* Tooltip */}
        {tooltip && (
          <Tooltip>
            <TooltipTrigger>
              <HelpCircle className="w-4 h-4 text-muted-foreground hover:text-foreground transition-colors" />
            </TooltipTrigger>
            <TooltipContent>
              <p className="max-w-xs">{tooltip}</p>
            </TooltipContent>
          </Tooltip>
        )}
      </div>
      
      {/* Description */}
      {description && (
        <p className="text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          {description}
        </p>
      )}
      
      {/* Children */}
      {children}
    </motion.div>
  );
}