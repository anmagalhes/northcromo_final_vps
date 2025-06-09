// src/hooks/useDefeitoWS.ts
'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

// URLs da API
const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/defeito`;
const WS_URL = 'ws://localhost:8000/api/ws/defeito';

// Interface atualizada com componente_nome
export interface Defeito {
  id: number;
  def_nome: string;
  data: string; // formato ISO ex: "2024-05-25T12:00:00Z"
  componente_id: number;
  componente_nome?: string; // agora incluído na resposta da API
}

// Função para buscar defeitos da API
const fetchDefeitos = async (): Promise<Defeito[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Erro ao buscar defeitos');
  return res.json();
};

// Hook customizado com WebSocket
export default function useDefeitoWS() {
  const queryClient = useQueryClient();

  const defeitosQuery = useQuery({
    queryKey: ['defeitos'],
    queryFn: fetchDefeitos,
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => console.log('✅ WebSocket Defeitos conectado');
    ws.onmessage = (event) => {
      if (event.data === 'update') {
        queryClient.invalidateQueries(['defeitos']);
      }
    };
    ws.onerror = (error) => console.error('❌ Erro WebSocket Defeitos:', error);
    ws.onclose = () => console.log('🔌 WebSocket Defeitos desconectado');

    return () => ws.close();
  }, [queryClient]);

  return {
    defeitosQuery,
  };
}
