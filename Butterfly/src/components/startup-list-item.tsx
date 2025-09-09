import { motion } from "framer-motion";
import { Startup } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ExternalLink, Building2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface StartupListItemProps {
  startup: Startup;
  index: number;
  className?: string;
}

export function StartupListItem({ startup, index, className }: StartupListItemProps) {
  const handleVisitWebsite = (e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(startup.website_url, '_blank', 'noopener,noreferrer');
  };

  // Create initials for logo fallback
  const initials = startup.name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      className={cn(
        "glass p-4 rounded-lg group hover:shadow-card transition-all duration-300",
        className
      )}
    >
      <div className="flex items-start gap-4">
        {/* Logo/Avatar */}
        <div className="flex-shrink-0">
          {startup.logo_url ? (
            <img
              src={startup.logo_url}
              alt={`${startup.name} logo`}
              className="w-12 h-12 rounded-lg object-cover bg-surface"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
                target.nextElementSibling?.classList.remove('hidden');
              }}
            />
          ) : null}
          
          {/* Fallback avatar */}
          <div 
            className={cn(
              "w-12 h-12 rounded-lg bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center border border-primary/10",
              startup.logo_url && "hidden"
            )}
          >
            {startup.logo_url ? (
              <Building2 className="w-6 h-6 text-primary/70" />
            ) : (
              <span className="text-sm font-medium text-primary/80">
                {initials}
              </span>
            )}
          </div>
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-start justify-between mb-2">
            <h4 className="font-semibold text-sm group-hover:text-primary transition-colors">
              {startup.name}
            </h4>
            
            <Button
              size="sm"
              variant="ghost"
              onClick={handleVisitWebsite}
              className="ml-2 opacity-70 hover:opacity-100 transition-opacity"
            >
              <ExternalLink className="w-3 h-3" />
            </Button>
          </div>
          
          {/* Description */}
          <p className="text-xs text-muted-foreground mb-3 leading-relaxed">
            {startup.one_liner}
          </p>
          
          {/* Tags */}
          <div className="flex flex-wrap gap-1">
            {startup.tags.slice(0, 3).map((tag, tagIndex) => (
              <Badge 
                key={tagIndex}
                variant="secondary" 
                className="text-xs px-2 py-0.5 bg-muted/30 hover:bg-muted/50 transition-colors"
              >
                {tag}
              </Badge>
            ))}
            {startup.tags.length > 3 && (
              <Badge 
                variant="outline" 
                className="text-xs px-2 py-0.5 opacity-60"
              >
                +{startup.tags.length - 3}
              </Badge>
            )}
          </div>
        </div>
      </div>
      
      {/* Hover effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none rounded-lg" />
    </motion.div>
  );
}