import React from 'react';
import { cn } from '@/lib/utils';

interface StatusGaugeProps {
  value: number;
  max?: number;
  label: string;
  color: 'primary' | 'success' | 'warning' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
}

export const StatusGauge: React.FC<StatusGaugeProps> = ({
  value,
  max = 100,
  label,
  color,
  size = 'md',
}) => {
  const percentage = (value / max) * 100;
  
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'primary':
        return 'text-primary';
      case 'success':
        return 'text-green-500';
      case 'warning':
        return 'text-yellow-500';
      case 'destructive':
        return 'text-red-500';
      default:
        return 'text-primary';
    }
  };

  const getSizeClasses = (size: string) => {
    switch (size) {
      case 'sm':
        return 'w-16 h-16';
      case 'lg':
        return 'w-32 h-32';
      default:
        return 'w-24 h-24';
    }
  };

  const getTextSizeClasses = (size: string) => {
    switch (size) {
      case 'sm':
        return 'text-xs';
      case 'lg':
        return 'text-2xl';
      default:
        return 'text-lg';
    }
  };

  return (
    <div className="flex flex-col items-center space-y-2">
      <div className="relative">
        <svg
          className={cn('transform -rotate-90', getSizeClasses(size))}
          viewBox="0 0 100 100"
        >
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            className="text-muted-foreground/20"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            fill="none"
            strokeDasharray={`${2 * Math.PI * 45}`}
            strokeDashoffset={`${2 * Math.PI * 45 * (1 - percentage / 100)}`}
            className={cn('transition-all duration-1000 ease-out', getColorClasses(color))}
            strokeLinecap="round"
          />
        </svg>
        
        {/* Center text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={cn('font-bold', getTextSizeClasses(size), getColorClasses(color))}>
            {value.toFixed(1)}
          </span>
        </div>
      </div>
      
      <div className="text-center">
        <div className="text-sm font-medium text-foreground">{label}</div>
        <div className="text-xs text-muted-foreground">
          {percentage.toFixed(1)}% of {max}
        </div>
      </div>
    </div>
  );
};


