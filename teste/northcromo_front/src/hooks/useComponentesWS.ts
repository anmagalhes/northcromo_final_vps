// src/hooks/useComponentesWS.ts
'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const baseURL = 'http://localhost:8000/api'

const API_URL = `${baseURL}/componente`;
const WS_URL = 'ws://localhost:8000/api/ws/componentes';

export interface Componente {
  id: number;
  componente_nome: string;
  data_recebimento: string;
}

const fetchComponentes = async (): Promise<Componente[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Erro ao buscar componentes');
  return res.json();
};

export default function useComponentesWS() {
  const queryClient = useQueryClient();

  const componentesQuery = useQuery({
    queryKey: ['componentes'],
    queryFn: fetchComponentes,
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('WebSocket conectado');
    };

    ws.onmessage = (event) => {
      if (event.data === 'update') {
        queryClient.invalidateQueries(['componentes']);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket erro:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket desconectado');
    };

    return () => {
      ws.close();
    };
  }, [queryClient]);

  return {
    componentesQuery,
  };
}

