// src/hooks/useProdutoTarefaWS.ts
'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/produto_tarefa`;
const WS_URL = 'ws://localhost:8000/api/ws/produto_tarefa';

export interface ProdutoTarefa {
  id: number;
  produto_taf_nome: string;
  data_execucao?: string; // ISO string opcional
}

const fetchProdutoTarefas = async (): Promise<ProdutoTarefa[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Erro ao buscar produto tarefas');
  return res.json();
};

export default function useProdutoTarefaWS() {
  const queryClient = useQueryClient();

  const produtoTarefaQuery = useQuery({
    queryKey: ['produto_tarefa'],
    queryFn: fetchProdutoTarefas,
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 5, // 5 minutos
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => console.log('✅ WebSocket Produto Tarefa conectado');

    ws.onmessage = (event) => {
      if (event.data === 'update') {
        queryClient.invalidateQueries(['produto_tarefa']);
      }
    };

    ws.onerror = (error) => console.error('❌ Erro WebSocket Produto Tarefa:', error);
    ws.onclose = () => console.log('🔌 WebSocket Produto Tarefa desconectado');

    return () => ws.close();
  }, [queryClient]);

  return {
    produtoTarefaQuery,
  };
}
