/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import { WSEvent } from '../lib/types';

interface UseWebSocketProps {
  url: string;
  token: string | null;
  onEvent?: (event: WSEvent) => void;
}

export function useWebSocket({ url, token, onEvent }: UseWebSocketProps) {
  const [connected, setConnected] = useState(false);
  const [lastEvent, setLastEvent] = useState<WSEvent | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const reconnectDelayRef = useRef(5000);

  const connect = useCallback(() => {
    if (!token) return;

    try {
      const wsUrl = `${url}?token=${token}`;
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnected(true);
        reconnectDelayRef.current = 5000; // Reset delay on success
      };

      ws.onmessage = (event) => {
        try {
          const data: WSEvent = JSON.parse(event.data);
          setLastEvent(data);
          if (onEvent) onEvent(data);
        } catch (err) {
          console.error('Failed to parse WebSocket message', err);
        }
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);
        socketRef.current = null;
        
        // Exponential backoff
        reconnectTimeoutRef.current = window.setTimeout(() => {
          reconnectDelayRef.current = Math.min(reconnectDelayRef.current * 2, 30000);
          connect();
        }, reconnectDelayRef.current);
      };

      ws.onerror = (err) => {
        console.error('WebSocket error', err);
        ws.close();
      };

      socketRef.current = ws;
    } catch (err) {
      console.error('WebSocket connection error', err);
    }
  }, [url, token, onEvent]);

  useEffect(() => {
    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect]);

  return { connected, lastEvent };
}
