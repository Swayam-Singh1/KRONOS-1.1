import React, { useState } from 'react';
import { DashboardHeader } from '@/components/DashboardHeader';
import { SystemOverview } from '@/components/SystemOverview';
import { EnginePanel } from '@/components/EnginePanel';
import { ThreatFeed } from '@/components/ThreatFeed';
import { Shield, Brain, Zap, Activity, AlertTriangle, Eye, RefreshCw } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useRealtimeData } from '@/hooks/use-realtime-data';

const Index = () => {
  const { toast } = useToast();
  const [systemStatus, setSystemStatus] = useState<'connected' | 'disconnected' | 'warning'>('connected');
  
  // Use real-time data hook
  const {
    systemStatus: systemOverviewData,
    orderEngine: orderEngineData,
    chaosEngine: chaosEngineData,
    balanceEngine: balanceEngineData,
    threatEvents,
    isConnected,
    isLoading,
    error,
    refreshAll
  } = useRealtimeData();

  // Update system status based on connection
  React.useEffect(() => {
    if (isConnected) {
      setSystemStatus('connected');
    } else {
      setSystemStatus('disconnected');
    }
  }, [isConnected]);

  // Show error toast if there's an error
  React.useEffect(() => {
    if (error) {
      toast({
        title: "Connection Error",
        description: "Failed to fetch real-time data. Using cached data.",
        variant: "destructive",
      });
    }
  }, [error, toast]);

  const handleRefresh = () => {
    refreshAll();
    toast({
      title: "System Refresh",
      description: "All systems refreshed successfully",
    });
  };

  const handleEmergencyStop = () => {
    setSystemStatus('disconnected');
    toast({
      title: "EMERGENCY STOP ACTIVATED",
      description: "All AI systems have been safely shutdown",
      variant: "destructive",
    });
  };

  const handleSettings = () => {
    toast({
      title: "Settings",
      description: "System configuration panel would open here",
    });
  };

  // Show loading state
  if (isLoading && !systemOverviewData) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Loading cybersecurity dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background grid effect */}
      <div className="absolute inset-0 grid-overlay opacity-30" />
      
      <div className="relative z-10 p-6 space-y-6">
        {/* Dashboard Header */}
        <DashboardHeader
          systemStatus={systemStatus}
          isConnected={isConnected}
          onRefresh={handleRefresh}
          onEmergencyStop={handleEmergencyStop}
          onSettings={handleSettings}
        />

        {/* System Overview */}
        <SystemOverview data={systemOverviewData || {
          balanceScore: 0.847,
          performanceHealth: 94.2,
          threatLevel: 23.5,
          totalSimulations: 1847293,
          successfulDefenses: 1646841,
          activeThreats: 3,
          systemUptime: "47d 12h 34m"
        }} />

        {/* Engine Panels */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <EnginePanel engine={orderEngineData || {
            name: "ORDER Engine",
            status: 'online' as const,
            description: "Defense & Threat Detection System",
            icon: Shield,
            primaryMetric: {
              value: 97.8,
              label: "Defense Accuracy",
              color: 'success' as const
            },
            metrics: [
              { label: "Flows Processed", value: "2.3M", change: "+12.4%", changeType: 'positive' as const },
              { label: "Anomalies Detected", value: "1,247", change: "+8 active", changeType: 'negative' as const },
              { label: "Model Mutations", value: "847", change: "Adaptive", changeType: 'neutral' as const },
              { label: "Response Time", value: "0.23ms", change: "-15%", changeType: 'positive' as const }
            ]
          }} />
          <EnginePanel engine={chaosEngineData || {
            name: "CHAOS Engine",
            status: 'online' as const,
            description: "Intelligence & Counterattack System",
            icon: Brain,
            primaryMetric: {
              value: 89.3,
              label: "Attack Success Rate",
              color: 'warning' as const
            },
            metrics: [
              { label: "OSINT Gathered", value: "45.7K", change: "+23.1%", changeType: 'positive' as const },
              { label: "Backdoors Found", value: "127", change: "6 critical", changeType: 'negative' as const },
              { label: "Target Analysis", value: "342", change: "Real-time", changeType: 'neutral' as const },
              { label: "Counter Ops", value: "28", change: "+5 today", changeType: 'positive' as const }
            ]
          }} />
          <EnginePanel engine={balanceEngineData || {
            name: "BALANCE Controller",
            status: 'online' as const,
            description: "AI Orchestration & Self-Morphing System",
            icon: Zap,
            primaryMetric: {
              value: 0.847,
              label: "AI Fitness Score",
              color: 'primary' as const
            },
            metrics: [
              { label: "Generation", value: "G47", change: "Evolving", changeType: 'neutral' as const },
              { label: "Learning Rate", value: "94.2%", change: "+2.3%", changeType: 'positive' as const },
              { label: "Adaptation Events", value: "1,234", change: "12 recent", changeType: 'neutral' as const },
              { label: "Neural Efficiency", value: "97.1%", change: "Optimal", changeType: 'positive' as const }
            ]
          }} />
        </div>

        {/* Real-Time Monitoring */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <ThreatFeed events={threatEvents || []} />
          </div>
          
          {/* Additional monitoring panel could go here */}
          <div className="space-y-4">
            {/* Future: Network topology, performance charts, etc. */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
