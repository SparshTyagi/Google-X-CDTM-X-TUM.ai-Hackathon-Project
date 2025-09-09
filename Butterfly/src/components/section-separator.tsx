import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SectionSeparatorProps {
  className?: string;
}

/**
 * Butterfly Section Separator - Premium animated divider
 * Creates visual breaks between major sections with subtle motion
 */
export function SectionSeparator({ className }: SectionSeparatorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scaleX: 0 }}
      whileInView={{ opacity: 1, scaleX: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      viewport={{ once: true, margin: "-100px" }}
      className={cn("py-8", className)}
    >
      <div className="section-separator" />
    </motion.div>
  );
}