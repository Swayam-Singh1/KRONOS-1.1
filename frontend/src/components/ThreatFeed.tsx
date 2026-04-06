import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { AlertTriangle, Shield, Eye, Zap, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ThreatEvent {
  id: string;
  timestamp: string;
  type: 'detection' | 'blocked' | 'investigation' | 'neutralized';
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  source: string;
  engine: 'ORDER' | 'CHAOS' | 'BALANCE';
}

interface ThreatFeedProps {
  events: ThreatEvent[];
}

export const ThreatFeed: React.FC<ThreatFeedProps> = ({ events }) => {
  const getEventIcon = (type: string) => {
    switch (type) {
      case 'detection':
        return Eye;
      case 'blocked':
        return Shield;
      case 'investigation':
        return AlertTriangle;
      case 'neutralized':
        return Zap;
      default:
        return AlertTriangle;
    }
  };

  const getEventColor = (type: string) => {
    switch (type) {
      case 'detection':
        return 'text-blue-500';
      case 'blocked':
        return 'text-green-500';
      case 'investigation':
        return 'text-yellow-500';
      case 'neutralized':
        return 'text-purple-500';
      default:
        return 'text-gray-500';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'low':
        return 'success';
      case 'medium':
        return 'warning';
      case 'high':
        return 'destructive';
      case 'critical':
        return 'destructive';
      default:
        return 'default';
    }
  };

  const getEngineColor = (engine: string) => {
    switch (engine) {
      case 'ORDER':
        return 'text-blue-500';
      case 'CHAOS':
        return 'text-red-500';
      case 'BALANCE':
        return 'text-purple-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <Card className="relative overflow-hidden bg-card/70 backdrop-blur-sm border-border/50">
      <div className="absolute inset-0 gradient-neural opacity-20" />
      
      <CardHeader className="relative z-10">
        <CardTitle className="text-xl font-bold flex items-center space-x-2">
          <AlertTriangle className="h-6 w-6 text-destructive" />
          <span>Real-Time Threat Feed</span>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="relative z-10">
        <ScrollArea className="h-[400px]">
          <div className="space-y-3">
            {events.map((event) => {
              const EventIcon = getEventIcon(event.type);
              
              return (
                <div
                  key={event.id}
                  className="flex items-start space-x-3 p-3 rounded-lg bg-muted/20 hover:bg-muted/40 transition-all duration-200 border border-border/30"
                >
                  <div className="flex-shrink-0">
                    <div className={cn('p-2 rounded-lg bg-muted/50', getEventColor(event.type))}>
                      <EventIcon className="h-4 w-4" />
                    </div>
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center space-x-2">
                        <Badge variant={getSeverityColor(event.severity) as any}>
                          {event.severity.toUpperCase()}
                        </Badge>
                        <Badge variant="outline" className={cn('text-xs', getEngineColor(event.engine))}>
                          {event.engine}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" />
                        <span>{event.timestamp}</span>
                      </div>
                    </div>
                    
                    <p className="text-sm font-medium text-foreground mb-1">
                      {event.description}
                    </p>
                    
                    <p className="text-xs text-muted-foreground">
                      Source: {event.source}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};


