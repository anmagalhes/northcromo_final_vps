// src/hooks/useProdutos.ts
'use client';

import { useQuery } from '@tanstack/react-query';

export type Produto = {
  codigo: string;
  nome: string;
};

export function useProdutos() {
  return useQuery<Produto[]>({
    queryKey: ['produtos'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/produtos');
      if (!res.ok) throw new Error('Erro ao buscar produtos');
      return res.json();
    },
    staleTime: 1000 * 60 * 10, // 10 minutos
  });
}
