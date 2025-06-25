// src/hooks/usePostoTrabalhoWS.ts
'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/posto_trabalho`;
const WS_URL = 'ws://localhost:8000/api/ws/postos_trabalho';

export interface PostoTrabalho {
id: number;
 posto_trabalho_nome: string;
}

const fetchPostosTrabalho = async (): Promise<PostoTrabalho[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Erro ao buscar postos de trabalho');
  return res.json();
};

export default function usePostoTrabalhoWS() {
  const queryClient = useQueryClient();

  const postostrabalhoQuery = useQuery({
    queryKey: ['postos_trabalho'],
    queryFn: fetchPostosTrabalho,
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => console.log('WebSocket Postos de Trabalho conectado');
    ws.onmessage = (event) => {
      if (event.data === 'update') {
        queryClient.invalidateQueries ({ queryKey: ['postos_trabalho'] });
      }
    };
    ws.onerror = (error) => console.error('Erro WebSocket Postos de Trabalho:', error);
    ws.onclose = () => console.log('WebSocket Postos de Trabalho desconectado');

    return () => ws.close();
  }, [queryClient]);

  return {
    postostrabalhoQuery,
  };
}
