// src/hooks/useOperacoesWS.ts
'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/operacao`;
const WS_URL = 'ws://localhost:8000/api/ws/operacoes';

export interface Operacao {
  id: number;
  op_nome: string;
  op_grupo_processo: string;
  data_execucao: string;
}

const fetchOperacoes = async (): Promise<Operacao[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Erro ao buscar operações');
  return res.json();
};

export default function useOperacoesWS() {
  const queryClient = useQueryClient();

  const operacoesQuery = useQuery({
    queryKey: ['operacoes'],
    queryFn: fetchOperacoes,
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => console.log('WebSocket Operações conectado');
    ws.onmessage = (event) => {
      if (event.data === 'update') {
        queryClient.invalidateQueries(['operacoes']);
      }
    };
    ws.onerror = (error) => console.error('Erro WebSocket Operações:', error);
    ws.onclose = () => console.log('WebSocket Operações desconectado');

    return () => ws.close();
  }, [queryClient]);

  return {
    operacoesQuery,
  };
}
