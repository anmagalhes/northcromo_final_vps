// src/hooks/useProdutosWS.ts
'use client';

import { useEffect } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const baseURL = 'http://localhost:8000/api';
const API_URL = `${baseURL}/produto`; // URL para os produtos
const WS_URL = 'ws://localhost:8000/api/ws/produtos'; // WebSocket para os produtos

interface Componente {
  id: number;
  componente_nome: string;
  // outros campos, se precisar
}

interface Operacao {
  id: number;
  operacao_nome: string;
  // outros campos
}

interface PostoTrabalho {
  id: number;
  posto_trabalho_nome: string;
  // outros campos
}

export interface Produto {
  id: number;
  cod_produto: string;
  produto_nome: string;
  und_servicos: string;
  grupo_id: 'PRODUTO' | 'SERVIÇO';
  tipo_produto: number;
  componente_id: number;
  operacao_id: number;
  posto_trabalho_id: number;
  componente?: Componente | null;
  operacao?: Operacao | null;
  posto_trabalho?: PostoTrabalho | null;
}

// Função para buscar os produtos do backend
const fetchProdutos = async (): Promise<Produto[]> => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error('Erro ao buscar produtos');
  return res.json();
};

export default function useProdutoWS() {
  const queryClient = useQueryClient();

  // Query dos produtos
  const produtosQuery = useQuery({
    queryKey: ['produtos'],
    queryFn: fetchProdutos,
    refetchOnWindowFocus: false, // Desativa refetch automático para evitar loops
    staleTime: 1000 * 60 * 5, // 5 minutos
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => console.log('✅ WebSocket Produtos conectado');

    ws.onmessage = (event) => {
      let data;

      try {
        data = JSON.parse(event.data); // Tenta parsear como JSON
      } catch {
        // Caso não seja JSON, usa o dado bruto
        data = event.data;
      }

      // Se o WS enviar um array de produtos atualizado
      if (Array.isArray(data)) {
        // Pega os dados atuais do cache do React Query
        const dadosAtuais = queryClient.getQueryData<Produto[]>(['produtos']);

        // Verifica se os dados são diferentes e atualiza o cache
        if (JSON.stringify(dadosAtuais) !== JSON.stringify(data)) {
          queryClient.setQueryData(['produtos'], data);
          console.log('Cache de produtos atualizado pelo WS');
        } else {
          console.log('Dados recebidos iguais ao cache, sem atualização');
        }
      } else if (typeof data === 'string' && data === 'update') {
        // Se o backend mandar só 'update', chama invalidate com debounce
        debounceInvalidate();
      } else {
        console.log('Mensagem WS não tratada:', data);
      }
    };

    ws.onerror = (error) => console.error('❌ Erro WebSocket Produtos:', error);
    ws.onclose = () => console.log('🔌 WebSocket Produtos desconectado');

    // Função para evitar múltiplos "invalidate" seguidos
    let invalidateTimeout: NodeJS.Timeout | null = null;
    const debounceInvalidate = () => {
      if (invalidateTimeout) return;
      invalidateTimeout = setTimeout(() => {
        queryClient.invalidateQueries(['produtos']);
        invalidateTimeout = null;
      }, 1000); // Debounce de 1 segundo
    };

    return () => {
      if (invalidateTimeout) clearTimeout(invalidateTimeout);
      ws.close();
    };
  }, [queryClient]);

  return { produtosQuery };
}
