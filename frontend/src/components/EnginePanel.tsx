import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MetricCard } from './MetricCard';
import { StatusGauge } from './StatusGauge';
import { LucideIcon, Activity, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface EnginePanelProps {
  engine: {
    name: string;
    status: 'online' | 'offline' | 'warning';
    description: string;
    icon: LucideIcon;
    primaryMetric: {
      value: number;
      label: string;
      color: 'primary' | 'success' | 'warning' | 'destructive';
    };
    metrics: Array<{
      label: string;
      value: string;
      change: string;
      changeType: 'positive' | 'negative' | 'neutral';
    }>;
  };
}

export const EnginePanel: React.FC<EnginePanelProps> = ({ engine }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online':
        return 'bg-green-500';
      case 'warning':
        return 'bg-yellow-500';
      case 'offline':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'online':
        return 'success';
      case 'warning':
        return 'warning';
      case 'offline':
        return 'destructive';
      default:
        return 'default';
    }
  };

  return (
    <Card className="relative overflow-hidden bg-card/70 backdrop-blur-sm border-border/50 hover:bg-card/80 transition-all duration-200">
      <div className="absolute inset-0 gradient-neural opacity-10" />
      
      <CardHeader className="relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <engine.icon className="h-6 w-6 text-primary" />
            </div>
            <div>
              <CardTitle className="text-lg font-bold">{engine.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{engine.description}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${getStatusColor(engine.status)} animate-pulse`} />
            <Badge variant={getStatusVariant(engine.status) as any}>
              {engine.status.toUpperCase()}
            </Badge>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="relative z-10 space-y-6">
        {/* Primary Metric Gauge */}
        <div className="flex justify-center">
          <StatusGauge
            value={engine.primaryMetric.value}
            label={engine.primaryMetric.label}
            color={engine.primaryMetric.color}
            size="md"
          />
        </div>
        
        {/* Secondary Metrics */}
        <div className="grid grid-cols-1 gap-3">
          {engine.metrics.map((metric, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  {metric.changeType === 'positive' && <TrendingUp className="h-4 w-4 text-green-500" />}
                  {metric.changeType === 'negative' && <TrendingDown className="h-4 w-4 text-red-500" />}
                  {metric.changeType === 'neutral' && <Minus className="h-4 w-4 text-muted-foreground" />}
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">{metric.label}</p>
                  <p className="text-lg font-bold text-primary">{metric.value}</p>
                </div>
              </div>
              <div className="text-right">
                <p className={cn(
                  'text-sm font-medium',
                  metric.changeType === 'positive' && 'text-green-500',
                  metric.changeType === 'negative' && 'text-red-500',
                  metric.changeType === 'neutral' && 'text-muted-foreground'
                )}>
                  {metric.change}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};


