'use client';

import { useEffect, useRef } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Tarefa } from '@/types/tarefas';

const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/novas-tarefas/tarefas`;
const WS_URL = 'ws://localhost:8000/api/novas-tarefas/ws/tarefa';

interface TarefaResponse {
  data: Tarefa[];
  page: number;
  limit: number;
  total: number;
  pages: number;
}

const fetchTarefas = async (page = 1, limit = 20): Promise<TarefaResponse> => {
  const res = await fetch(`${API_URL}?page=${page}&limit=${limit}`);
  if (!res.ok) throw new Error('Erro ao buscar tarefas');
  return res.json();
};

export default function useNovaTarefasWS(page = 1, limit = 20) {
  const queryClient = useQueryClient();

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const debounceTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const tarefasQuery = useQuery({
    queryKey: ['tarefas', page, limit],
    queryFn: () => fetchTarefas(page, limit),
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    const connectWebSocket = () => {
      if (wsRef.current) {
        wsRef.current.close();
      }

      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('✅ WebSocket conectado');
      };

      ws.onerror = (error) => {
        console.error('❌ Erro no WebSocket:', error);
      };

      ws.onmessage = (event) => {
        const message = event.data;
        console.log('WS message recebida:', message);
        if (message === 'update') {
          debounceInvalidate();
        }
      };

      ws.onclose = () => {
        console.log('🔌 WebSocket desconectado. Reconectando em 5s...');
        if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
        reconnectTimeoutRef.current = setTimeout(connectWebSocket, 5000);
      };
    };

    const debounceInvalidate = () => {
      if (debounceTimeoutRef.current) return;
      debounceTimeoutRef.current = setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['tarefas', page, limit] });
        debounceTimeoutRef.current = null;
      }, 1000);
    };

    connectWebSocket();

    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (debounceTimeoutRef.current) clearTimeout(debounceTimeoutRef.current);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  // ⚠️ aqui removemos tarefasQuery.data das dependências, mantendo só o que é necessário:
  }, [queryClient, page, limit]);

  return {
    tarefas: tarefasQuery.data?.data ?? [],
    pageInfo: {
      page: tarefasQuery.data?.page ?? page,
      limit: tarefasQuery.data?.limit ?? limit,
      total: tarefasQuery.data?.total ?? 0,
      pages: tarefasQuery.data?.pages ?? 0,
    },
    isLoading: tarefasQuery.isLoading,
    isError: tarefasQuery.isError,
    refetch: tarefasQuery.refetch,
  };
}
