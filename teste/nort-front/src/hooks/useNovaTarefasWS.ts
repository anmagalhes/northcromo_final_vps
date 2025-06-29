// src/hooks/useNovaTarefasWS.ts

'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Tarefa } from '@/types/tarefas';

const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/novas-tarefas`;
const WS_URL = 'ws://localhost:8000/api/ws/novas-tarefas';

interface TarefaResponse {
  data: Tarefa[];
  page: number;
  limit: number;
  total: number;
  pages: number;
}

// Função para buscar as tarefas com paginação
const fetchTarefas = async (
  page = 1,
  limit = 20
): Promise<TarefaResponse> => {
  const res = await fetch(`${API_URL}?page=${page}&limit=${limit}`);
  if (!res.ok) throw new Error('Erro ao buscar tarefas');
  return res.json();
};

export default function useNovaTarefasWS(page = 1, limit = 20) {
  const queryClient = useQueryClient();

  const tarefasQuery = useQuery({
    queryKey: ['tarefas', page, limit],
    queryFn: () => fetchTarefas(page, limit),
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    console.log('🔌 Conectando ao WS Nova Tarefas...');

    ws.onopen = () => console.log('✅ WebSocket Tarefa conectado');
    ws.onerror = (error) => console.error('❌ Erro WebSocket Tarefa:', error);
    ws.onclose = () => console.log('🔌 WebSocket Tarefa desconectado');

    ws.onmessage = (event) => {
      const message = event.data;

      if (message === 'update') {
        debounceInvalidate();
      } else {
        console.log('📩 WS Tarefa - Mensagem não tratada:', message);
      }
    };

    let timeout: NodeJS.Timeout | null = null;
    const debounceInvalidate = () => {
      if (timeout) return;
      timeout = setTimeout(() => {
        queryClient.invalidateQueries({
          queryKey: ['tarefas', page, limit],
        });
        timeout = null;
      }, 1000);
    };

    return () => {
      if (timeout) clearTimeout(timeout);
      ws.close();
    };
  }, [queryClient, page, limit]);

  return { tarefasQuery };
}
