'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

// Função para criar cliente (exemplo simples)
async function createCliente(novoCliente: any) {
  const response = await fetch('http://localhost:8000/clientes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(novoCliente),
  });

  if (!response.ok) {
    throw new Error('Erro ao criar cliente');
  }

  return response.json();
}

export default function useClientes() {
  const queryClient = useQueryClient();

  const clientesQuery = useQuery({
    queryKey: ['clientes'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/clientes');
      if (!response.ok) throw new Error('Erro ao buscar clientes');
      return response.json();
    },
    staleTime: 1000 * 60 * 10, // 10 minutos
  });

  const clientesMutation = useMutation({
    mutationFn: createCliente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clientes'] });
    },
  });

  return {
    clientesQuery,
    clientesMutation,
  };
}
