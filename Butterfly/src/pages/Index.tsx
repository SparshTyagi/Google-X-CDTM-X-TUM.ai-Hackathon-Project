import { useState } from "react";
import { Subtrend } from "@/types";
import { ButterflyHeader } from "@/components/butterfly-header";
import { HeroSection } from "@/components/hero-section";
import { SubtrendsSection } from "@/components/subtrends-section";
import { SubtrendDetailDrawer } from "@/components/subtrend-detail-drawer";
import { SectionSeparator } from "@/components/section-separator";
import { SettingsPanel } from "@/components/settings-panel";

const Index = () => {
  const [selectedTrendId, setSelectedTrendId] = useState<string | null>(null);
  const [selectedSubtrend, setSelectedSubtrend] = useState<Subtrend | null>(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);

  const handleExploreClick = (trendId: string) => {
    setSelectedTrendId(trendId);
    
    // Scroll to subtrends section
    const subtrendsSection = document.getElementById('subtrends-section');
    if (subtrendsSection) {
      subtrendsSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSubtrendClick = (subtrend: Subtrend) => {
    setSelectedSubtrend(subtrend);
    setIsDetailOpen(true);
  };

  const handleCloseDetail = () => {
    setIsDetailOpen(false);
    setSelectedSubtrend(null);
  };

  return (
    <main className="min-h-screen">
      {/* Settings Panel */}
      <SettingsPanel />
      
      {/* Butterfly Header */}
      <ButterflyHeader />
      
      {/* Hero Section */}
      <HeroSection onExploreClick={handleExploreClick} />
      
      {/* Section Separator */}
      <SectionSeparator />
      
      {/* Subtrends Section */}
      <SubtrendsSection
        selectedTrendId={selectedTrendId}
        onSubtrendClick={handleSubtrendClick}
      />
      
      {/* Section Separator */}
      <SectionSeparator />
      
      {/* Subtrend Detail Drawer */}
      <SubtrendDetailDrawer
        subtrend={selectedSubtrend}
        isOpen={isDetailOpen}
        onClose={handleCloseDetail}
      />
    </main>
  );
};

export default Index;
