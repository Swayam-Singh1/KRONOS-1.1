import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { StatusGauge } from './StatusGauge';
import { MetricCard } from './MetricCard';
import { Shield, Activity, AlertTriangle, Clock } from 'lucide-react';

interface SystemOverviewProps {
  data: {
    balanceScore: number;
    performanceHealth: number;
    threatLevel: number;
    totalSimulations: number;
    successfulDefenses: number;
    activeThreats: number;
    systemUptime: string;
  };
}

export const SystemOverview: React.FC<SystemOverviewProps> = ({ data }) => {
  const getThreatLevelColor = (level: number) => {
    if (level < 30) return 'success';
    if (level < 70) return 'warning';
    return 'destructive';
  };

  return (
    <Card className="relative overflow-hidden bg-card/70 backdrop-blur-sm border-border/50">
      <div className="absolute inset-0 gradient-neural opacity-20" />
      
      <CardHeader className="relative z-10">
        <CardTitle className="text-xl font-bold flex items-center space-x-2">
          <Activity className="h-6 w-6 text-primary" />
          <span>System Overview</span>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {/* Main Gauges */}
          <div className="flex justify-center">
            <StatusGauge
              value={data.balanceScore}
              max={1}
              label="System Balance Score"
              color="primary"
              size="lg"
            />
          </div>
          
          <div className="flex justify-center">
            <StatusGauge
              value={data.performanceHealth}
              label="Performance Health"
              color="success"
              size="lg"
            />
          </div>
          
          <div className="flex justify-center">
            <StatusGauge
              value={data.threatLevel}
              label="Threat Level"
              color={getThreatLevelColor(data.threatLevel)}
              size="lg"
            />
          </div>
        </div>
        
        {/* Key Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
          <MetricCard
            title="Total Simulations"
            value={data.totalSimulations.toLocaleString()}
            change="+1,247 today"
            changeType="positive"
            icon={Activity}
          />
          
          <MetricCard
            title="Successful Defenses"
            value={data.successfulDefenses.toLocaleString()}
            change="+89.2% success rate"
            changeType="positive"
            icon={Shield}
          />
          
          <MetricCard
            title="Active Threats"
            value={data.activeThreats}
            change={data.activeThreats > 5 ? "High activity" : "Low activity"}
            changeType={data.activeThreats > 5 ? "negative" : "positive"}
            icon={AlertTriangle}
          />
          
          <MetricCard
            title="System Uptime"
            value={data.systemUptime}
            change="99.9% availability"
            changeType="positive"
            icon={Clock}
          />
        </div>
      </CardContent>
    </Card>
  );
};


