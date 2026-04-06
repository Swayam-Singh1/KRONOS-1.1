import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string | number;
  change: string;
  changeType: 'positive' | 'negative' | 'neutral';
  icon: LucideIcon;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  changeType,
  icon: Icon,
}) => {
  const getChangeIcon = (type: string) => {
    switch (type) {
      case 'positive':
        return TrendingUp;
      case 'negative':
        return TrendingDown;
      default:
        return Minus;
    }
  };

  const getChangeColor = (type: string) => {
    switch (type) {
      case 'positive':
        return 'text-green-500';
      case 'negative':
        return 'text-red-500';
      default:
        return 'text-muted-foreground';
    }
  };

  const ChangeIcon = getChangeIcon(changeType);

  return (
    <Card className="relative overflow-hidden bg-card/50 backdrop-blur-sm border-border/30 hover:bg-card/70 transition-all duration-200">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <Icon className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">{title}</p>
              <p className="text-2xl font-bold text-foreground">{value}</p>
            </div>
          </div>
        </div>
        
        <div className="mt-3 flex items-center space-x-2">
          <ChangeIcon className={cn('h-4 w-4', getChangeColor(changeType))} />
          <span className={cn('text-sm font-medium', getChangeColor(changeType))}>
            {change}
          </span>
        </div>
      </CardContent>
    </Card>
  );
};


