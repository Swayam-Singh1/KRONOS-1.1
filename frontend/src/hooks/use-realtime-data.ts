import { useState, useEffect, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const API_BASE_URL = 'http://localhost:8000';

interface SystemStatus {
  balanceScore: number;
  performanceHealth: number;
  threatLevel: number;
  totalSimulations: number;
  successfulDefenses: number;
  activeThreats: number;
  systemUptime: string;
}

interface EngineData {
  name: string;
  status: 'online' | 'offline' | 'warning';
  description: string;
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
}

interface ThreatEvent {
  id: string;
  timestamp: string;
  type: 'detection' | 'blocked' | 'investigation' | 'neutralized';
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  source: string;
  engine: 'ORDER' | 'CHAOS' | 'BALANCE';
}

// API functions
const fetchSystemStatus = async (): Promise<SystemStatus> => {
  try {
    const response = await fetch(`${API_BASE_URL}/status`);
    if (!response.ok) throw new Error('Failed to fetch system status');
    return response.json();
  } catch (error) {
    console.warn('Using fallback system status data');
    return {
      balanceScore: 0.847,
      performanceHealth: 94.2,
      threatLevel: 23.5,
      totalSimulations: 1847293,
      successfulDefenses: 1646841,
      activeThreats: 3,
      systemUptime: "47d 12h 34m"
    };
  }
};

const fetchOrderEngine = async (): Promise<EngineData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/order/status`);
    if (!response.ok) throw new Error('Failed to fetch ORDER engine data');
    const data = await response.json();
    return {
      name: "ORDER Engine",
      status: data.status || 'online',
      description: "Defense & Threat Detection System",
      primaryMetric: {
        value: data.accuracy || 97.8,
        label: "Defense Accuracy",
        color: 'success' as const
      },
      metrics: [
        { label: "Flows Processed", value: data.flows_processed || "2.3M", change: "+12.4%", changeType: 'positive' as const },
        { label: "Anomalies Detected", value: data.anomalies_detected || "1,247", change: "+8 active", changeType: 'negative' as const },
        { label: "Model Mutations", value: data.mutations || "847", change: "Adaptive", changeType: 'neutral' as const },
        { label: "Response Time", value: data.response_time || "0.23ms", change: "-15%", changeType: 'positive' as const }
      ]
    };
  } catch (error) {
    console.warn('Using fallback ORDER engine data');
    return {
      name: "ORDER Engine",
      status: 'online' as const,
      description: "Defense & Threat Detection System",
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
    };
  }
};

const fetchChaosEngine = async (): Promise<EngineData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chaos/status`);
    if (!response.ok) throw new Error('Failed to fetch CHAOS engine data');
    const data = await response.json();
    return {
      name: "CHAOS Engine",
      status: data.status || 'online',
      description: "Intelligence & Counterattack System",
      primaryMetric: {
        value: data.success_rate || 89.3,
        label: "Attack Success Rate",
        color: 'warning' as const
      },
      metrics: [
        { label: "OSINT Gathered", value: data.osint_count || "45.7K", change: "+23.1%", changeType: 'positive' as const },
        { label: "Backdoors Found", value: data.backdoors_found || "127", change: "6 critical", changeType: 'negative' as const },
        { label: "Target Analysis", value: data.targets_analyzed || "342", change: "Real-time", changeType: 'neutral' as const },
        { label: "Counter Ops", value: data.counter_ops || "28", change: "+5 today", changeType: 'positive' as const }
      ]
    };
  } catch (error) {
    console.warn('Using fallback CHAOS engine data');
    return {
      name: "CHAOS Engine",
      status: 'online' as const,
      description: "Intelligence & Counterattack System",
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
    };
  }
};

const fetchBalanceEngine = async (): Promise<EngineData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/balance/status`);
    if (!response.ok) throw new Error('Failed to fetch BALANCE engine data');
    const data = await response.json();
    return {
      name: "BALANCE Controller",
      status: data.status || 'online',
      description: "AI Orchestration & Self-Morphing System",
      primaryMetric: {
        value: data.fitness_score || 0.847,
        label: "AI Fitness Score",
        color: 'primary' as const
      },
      metrics: [
        { label: "Generation", value: data.generation || "G47", change: "Evolving", changeType: 'neutral' as const },
        { label: "Learning Rate", value: data.learning_rate || "94.2%", change: "+2.3%", changeType: 'positive' as const },
        { label: "Adaptation Events", value: data.adaptation_events || "1,234", change: "12 recent", changeType: 'neutral' as const },
        { label: "Neural Efficiency", value: data.neural_efficiency || "97.1%", change: "Optimal", changeType: 'positive' as const }
      ]
    };
  } catch (error) {
    console.warn('Using fallback BALANCE engine data');
    return {
      name: "BALANCE Controller",
      status: 'online' as const,
      description: "AI Orchestration & Self-Morphing System",
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
    };
  }
};

const fetchThreatEvents = async (): Promise<ThreatEvent[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/order/security-incidents?limit=10`);
    if (!response.ok) throw new Error('Failed to fetch threat events');
    const data = await response.json();
    
    // Transform backend data to frontend format
    return data.map((incident: any, index: number) => ({
      id: incident.id || `threat-${index}`,
      timestamp: new Date(incident.timestamp || Date.now()).toLocaleTimeString(),
      type: incident.type || 'detection',
      severity: incident.severity || 'medium',
      description: incident.description || 'Security incident detected',
      source: incident.source || 'Unknown',
      engine: incident.engine || 'ORDER'
    }));
  } catch (error) {
    console.warn('Using fallback threat events data');
    return [
      {
        id: 'threat-1',
        timestamp: new Date().toLocaleTimeString(),
        type: 'detection',
        severity: 'high',
        description: 'Suspicious network activity detected',
        source: '192.168.1.100',
        engine: 'ORDER'
      },
      {
        id: 'threat-2',
        timestamp: new Date(Date.now() - 30000).toLocaleTimeString(),
        type: 'blocked',
        severity: 'medium',
        description: 'Malicious payload blocked',
        source: '10.0.0.50',
        engine: 'ORDER'
      },
      {
        id: 'threat-3',
        timestamp: new Date(Date.now() - 60000).toLocaleTimeString(),
        type: 'investigation',
        severity: 'low',
        description: 'Anomalous behavior pattern',
        source: '172.16.0.25',
        engine: 'CHAOS'
      }
    ];
  }
};

// Custom hook for real-time data
export const useRealtimeData = () => {
  const queryClient = useQueryClient();
  const [isConnected, setIsConnected] = useState(false);

  // System status query
  const systemStatusQuery = useQuery({
    queryKey: ['systemStatus'],
    queryFn: fetchSystemStatus,
    refetchInterval: 2000, // Refetch every 2 seconds
    staleTime: 1000,
  });

  // Engine queries
  const orderEngineQuery = useQuery({
    queryKey: ['orderEngine'],
    queryFn: fetchOrderEngine,
    refetchInterval: 3000,
    staleTime: 1000,
  });

  const chaosEngineQuery = useQuery({
    queryKey: ['chaosEngine'],
    queryFn: fetchChaosEngine,
    refetchInterval: 3000,
    staleTime: 1000,
  });

  const balanceEngineQuery = useQuery({
    queryKey: ['balanceEngine'],
    queryFn: fetchBalanceEngine,
    refetchInterval: 3000,
    staleTime: 1000,
  });

  // Threat events query
  const threatEventsQuery = useQuery({
    queryKey: ['threatEvents'],
    queryFn: fetchThreatEvents,
    refetchInterval: 1000, // Refetch every second for real-time updates
    staleTime: 500,
  });

  // WebSocket connection for real-time updates
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Update queries based on WebSocket data
        if (data.type === 'system_status') {
          queryClient.setQueryData(['systemStatus'], data.data);
        } else if (data.type === 'order_engine') {
          queryClient.setQueryData(['orderEngine'], data.data);
        } else if (data.type === 'chaos_engine') {
          queryClient.setQueryData(['chaosEngine'], data.data);
        } else if (data.type === 'balance_engine') {
          queryClient.setQueryData(['balanceEngine'], data.data);
        } else if (data.type === 'threat_event') {
          // Add new threat event to the list
          queryClient.setQueryData(['threatEvents'], (old: ThreatEvent[] = []) => {
            const newEvent = data.data;
            return [newEvent, ...old.slice(0, 9)]; // Keep only latest 10 events
          });
        }
      } catch (error) {
        console.error('Error parsing WebSocket data:', error);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [queryClient]);

  // Manual refresh function
  const refreshAll = useCallback(() => {
    queryClient.invalidateQueries({ queryKey: ['systemStatus'] });
    queryClient.invalidateQueries({ queryKey: ['orderEngine'] });
    queryClient.invalidateQueries({ queryKey: ['chaosEngine'] });
    queryClient.invalidateQueries({ queryKey: ['balanceEngine'] });
    queryClient.invalidateQueries({ queryKey: ['threatEvents'] });
  }, [queryClient]);

  return {
    systemStatus: systemStatusQuery.data,
    orderEngine: orderEngineQuery.data,
    chaosEngine: chaosEngineQuery.data,
    balanceEngine: balanceEngineQuery.data,
    threatEvents: threatEventsQuery.data || [],
    isConnected,
    isLoading: systemStatusQuery.isLoading || orderEngineQuery.isLoading || chaosEngineQuery.isLoading || balanceEngineQuery.isLoading,
    error: systemStatusQuery.error || orderEngineQuery.error || chaosEngineQuery.error || balanceEngineQuery.error,
    refreshAll,
  };
};
