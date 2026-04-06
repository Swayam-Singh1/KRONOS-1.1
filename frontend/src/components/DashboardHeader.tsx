import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Shield, RefreshCw, AlertTriangle, Settings, Power } from 'lucide-react';

interface DashboardHeaderProps {
  systemStatus: 'connected' | 'disconnected' | 'warning';
  isConnected?: boolean;
  onRefresh: () => void;
  onEmergencyStop: () => void;
  onSettings: () => void;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  systemStatus,
  isConnected = false,
  onRefresh,
  onEmergencyStop,
  onSettings,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
        return 'bg-green-500';
      case 'warning':
        return 'bg-yellow-500';
      case 'disconnected':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'connected':
        return 'Online';
      case 'warning':
        return 'Warning';
      case 'disconnected':
        return 'Offline';
      default:
        return 'Unknown';
    }
  };

  return (
    <Card className="relative overflow-hidden bg-card/70 backdrop-blur-sm border-border/50">
      <div className="absolute inset-0 gradient-neural opacity-20" />
      
      <CardContent className="relative z-10 p-6">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Shield className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  Self-Morphing AI Cybersecurity Engine
                </h1>
                <p className="text-sm text-muted-foreground">
                  Professional Cybersecurity Defense Platform v3.0
                </p>
              </div>
            </div>
          </div>

          {/* Status and Controls */}
          <div className="flex items-center space-x-4">
            {/* Real-time Connection Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
              <Badge variant={isConnected ? 'success' : 'destructive'}>
                {isConnected ? 'LIVE' : 'OFFLINE'}
              </Badge>
            </div>
            
            {/* System Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${getStatusColor(systemStatus)} animate-pulse`} />
              <Badge variant={systemStatus === 'connected' ? 'default' : 'destructive'}>
                {getStatusText(systemStatus)}
              </Badge>
            </div>

            {/* Control Buttons */}
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={onRefresh}
                className="hover:bg-primary/10"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>

              <Button
                variant="outline"
                size="sm"
                onClick={onSettings}
                className="hover:bg-primary/10"
              >
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>

              <Button
                variant="destructive"
                size="sm"
                onClick={onEmergencyStop}
                className="hover:bg-destructive/90"
              >
                <Power className="h-4 w-4 mr-2" />
                Emergency Stop
              </Button>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="mt-4 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary">3</div>
            <div className="text-sm text-muted-foreground">Active Engines</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-success">99.9%</div>
            <div className="text-sm text-muted-foreground">Uptime</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-warning">23</div>
            <div className="text-sm text-muted-foreground">Active Threats</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-primary">1.8M</div>
            <div className="text-sm text-muted-foreground">Simulations</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
