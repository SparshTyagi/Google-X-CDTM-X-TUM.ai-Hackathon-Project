import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { testConnection, clearCache } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Settings, Wifi, WifiOff, Database, Trash2, Save, AlertCircle, CheckCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export function SettingsPanel() {
  const [isOpen, setIsOpen] = useState(false);
  const [apiUrl, setApiUrl] = useState('');
  const [useMocks, setUseMocks] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState<{
    testing: boolean;
    success?: boolean;
    latency?: number;
    error?: string;
  }>({ testing: false });
  const { toast } = useToast();

  // Load settings from localStorage
  useEffect(() => {
    const savedApiUrl = localStorage.getItem('apiBaseUrl') || '';
    const savedUseMocks = localStorage.getItem('useMocks') !== 'false';
    
    setApiUrl(savedApiUrl);
    setUseMocks(savedUseMocks);
  }, []);

  const handleSaveSettings = () => {
    // Save to localStorage
    if (apiUrl.trim()) {
      localStorage.setItem('apiBaseUrl', apiUrl.trim());
    } else {
      localStorage.removeItem('apiBaseUrl');
    }
    
    localStorage.setItem('useMocks', useMocks.toString());
    
    // Clear cache when settings change
    clearCache();
    
    toast({
      title: "Settings saved",
      description: "API configuration updated successfully",
    });
  };

  const handleTestConnection = async () => {
    setConnectionStatus({ testing: true });
    
    try {
      const result = await testConnection();
      
      if (result.success) {
        setConnectionStatus({
          testing: false,
          success: true,
          latency: result.latency
        });
        
        toast({
          title: "Connection successful",
          description: `Response time: ${result.latency}ms`,
        });
      } else {
        setConnectionStatus({
          testing: false,
          success: false,
          error: result.error
        });
        
        toast({
          variant: "destructive",
          title: "Connection failed",
          description: result.error,
        });
      }
    } catch (error) {
      setConnectionStatus({
        testing: false,
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
      
      toast({
        variant: "destructive",
        title: "Connection test failed",
        description: "Unable to test connection",
      });
    }
  };

  const handleClearCache = () => {
    clearCache();
    toast({
      title: "Cache cleared",
      description: "All cached data has been removed",
    });
  };

  const getConnectionBadge = () => {
    if (connectionStatus.testing) {
      return (
        <Badge variant="secondary" className="gap-1">
          <div className="w-2 h-2 bg-current rounded-full animate-pulse" />
          Testing...
        </Badge>
      );
    }
    
    if (connectionStatus.success === true) {
      return (
        <Badge variant="default" className="bg-momentum-up/10 text-momentum-up border-momentum-up/20 gap-1">
          <CheckCircle className="w-3 h-3" />
          Connected ({connectionStatus.latency}ms)
        </Badge>
      );
    }
    
    if (connectionStatus.success === false) {
      return (
        <Badge variant="destructive" className="gap-1">
          <AlertCircle className="w-3 h-3" />
          Failed
        </Badge>
      );
    }
    
    return (
      <Badge variant="outline" className="gap-1">
        <Database className="w-3 h-3" />
        Not tested
      </Badge>
    );
  };

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button
          variant="ghost"
          size="sm"
          className="fixed top-4 right-4 z-40 glass"
        >
          <Settings className="w-4 h-4" />
        </Button>
      </SheetTrigger>
      
      <SheetContent side="right" className="w-full sm:max-w-md">
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            Settings
          </SheetTitle>
        </SheetHeader>
        
        <div className="py-6 space-y-6">
          {/* API Configuration */}
          <div className="space-y-4">
            <div>
              <Label htmlFor="api-url" className="text-sm font-medium">
                API Base URL
              </Label>
              <p className="text-xs text-muted-foreground mt-1">
                Backend API endpoint for live data
              </p>
            </div>
            
            <div className="space-y-3">
              <Input
                id="api-url"
                type="url"
                placeholder="https://api.trendscouter.com"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
              />
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Switch
                    id="use-mocks"
                    checked={useMocks}
                    onCheckedChange={setUseMocks}
                  />
                  <Label htmlFor="use-mocks" className="text-sm">
                    Use local mocks
                  </Label>
                </div>
                
                {getConnectionBadge()}
              </div>
            </div>
          </div>
          
          {/* Connection Status */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Connection Status</Label>
            
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleTestConnection}
                disabled={connectionStatus.testing || (!apiUrl.trim() && !useMocks)}
                className="flex-1"
              >
                {connectionStatus.testing ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-4 h-4 mr-2"
                  >
                    <Wifi className="w-4 h-4" />
                  </motion.div>
                ) : (
                  <Wifi className="w-4 h-4 mr-2" />
                )}
                Test Connection
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleClearCache}
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
            
            {connectionStatus.error && (
              <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                <p className="text-xs text-destructive">{connectionStatus.error}</p>
              </div>
            )}
          </div>
          
          {/* Data Source Info */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Data Source</Label>
            
            <div className="p-3 glass rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Current source:</span>
                <Badge variant={useMocks ? "secondary" : "default"}>
                  {useMocks ? "Local Mocks" : "Live API"}
                </Badge>
              </div>
              
              {!useMocks && apiUrl && (
                <div className="text-xs text-muted-foreground break-all">
                  {apiUrl}
                </div>
              )}
            </div>
          </div>
          
          {/* Actions */}
          <div className="flex gap-2 pt-4">
            <Button onClick={handleSaveSettings} className="flex-1">
              <Save className="w-4 h-4 mr-2" />
              Save Settings
            </Button>
          </div>
          
          {/* Help */}
          <div className="text-xs text-muted-foreground space-y-1">
            <p>• Use local mocks to run without a backend</p>
            <p>• Configure API URL to connect to your GCP backend</p>
            <p>• Clear cache to refresh data</p>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}