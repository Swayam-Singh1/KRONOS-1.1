import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Activity, TrendingUp, TrendingDown } from 'lucide-react';

interface ChartDataPoint {
  timestamp: string;
  value: number;
  label: string;
}

interface RealtimeChartProps {
  title: string;
  data: ChartDataPoint[];
  color?: string;
  type?: 'line' | 'area';
  maxDataPoints?: number;
}

export const RealtimeChart: React.FC<RealtimeChartProps> = ({
  title,
  data,
  color = '#3b82f6',
  type = 'line',
  maxDataPoints = 20
}) => {
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);

  useEffect(() => {
    // Keep only the latest data points
    const recentData = data.slice(-maxDataPoints);
    setChartData(recentData);
  }, [data, maxDataPoints]);

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getTrend = () => {
    if (chartData.length < 2) return 'neutral';
    const first = chartData[0].value;
    const last = chartData[chartData.length - 1].value;
    return last > first ? 'up' : last < first ? 'down' : 'neutral';
  };

  const trend = getTrend();
  const currentValue = chartData[chartData.length - 1]?.value || 0;

  return (
    <Card className="relative overflow-hidden bg-card/70 backdrop-blur-sm border-border/50">
      <div className="absolute inset-0 gradient-neural opacity-10" />
      
      <CardHeader className="relative z-10">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-bold">{title}</CardTitle>
          <div className="flex items-center space-x-2">
            {trend === 'up' && <TrendingUp className="h-4 w-4 text-green-500" />}
            {trend === 'down' && <TrendingDown className="h-4 w-4 text-red-500" />}
            {trend === 'neutral' && <Activity className="h-4 w-4 text-muted-foreground" />}
            <span className="text-sm font-medium text-foreground">
              {currentValue.toFixed(1)}
            </span>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="relative z-10">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            {type === 'area' ? (
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis 
                  dataKey="timestamp" 
                  tickFormatter={formatTime}
                  className="text-xs"
                />
                <YAxis className="text-xs" />
                <Tooltip 
                  labelFormatter={(value) => `Time: ${formatTime(value)}`}
                  formatter={(value) => [value, 'Value']}
                />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke={color}
                  fill={color}
                  fillOpacity={0.2}
                  strokeWidth={2}
                />
              </AreaChart>
            ) : (
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                <XAxis 
                  dataKey="timestamp" 
                  tickFormatter={formatTime}
                  className="text-xs"
                />
                <YAxis className="text-xs" />
                <Tooltip 
                  labelFormatter={(value) => `Time: ${formatTime(value)}`}
                  formatter={(value) => [value, 'Value']}
                />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={color}
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 4, fill: color }}
                />
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};


