/**
 * WebSocket hook for real-time communication
 */

import { useEffect, useRef, useState } from 'react';
import { WS_URL } from '../constants/config';

interface UseWebSocketOptions {
  onMessage?: (data: any) => void;
  onError?: (error: Event) => void;
  onClose?: () => void;
  reconnect?: boolean;
  reconnectInterval?: number;
}

export function useWebSocket(endpoint: string, options: UseWebSocketOptions = {}) {
  const {
    onMessage,
    onError,
    onClose,
    reconnect = true,
    reconnectInterval = 5000,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  const connect = () => {
    try {
      const token = localStorage.getItem('access_token');
      const url = `${WS_URL}${endpoint}${token ? `?token=${token}` : ''}`;

      wsRef.current = new WebSocket(url);

      wsRef.current.onopen = () => {
        setIsConnected(true);
        console.log('WebSocket connected');
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setLastMessage(data);
          onMessage?.(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        onError?.(error);
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket disconnected');
        onClose?.();

        // Attempt to reconnect
        if (reconnect) {
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
    }
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    wsRef.current?.close();
  };

  const sendMessage = (data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    } else {
      console.error('WebSocket is not connected');
    }
  };

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [endpoint]);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    disconnect,
  };
}
