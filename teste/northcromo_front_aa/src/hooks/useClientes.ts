// src/hooks/useClientes.ts
'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

// Corrigir URL da API
const API_URL = 'http://localhost:8000/api/clientes'; // Adicionar /api

interface Cliente {
  id: number;
  nome: string;
  email: string;
  telefone?: string;
}

async function fetchClientes(): Promise<Cliente[]> {
  const response = await fetch(API_URL); // Usar URL corrigida
  if (!response.ok) throw new Error('Erro ao buscar clientes');
  return response.json();
}

async function createCliente(novoCliente: Omit<Cliente, 'id'>): Promise<Cliente> {
  const response = await fetch(API_URL, { // Usar URL corrigida
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(novoCliente),
  });

  if (!response.ok) throw new Error('Erro ao criar cliente');
  return response.json();
}

export default function useClientes() {
  const queryClient = useQueryClient();

  const clientesQuery = useQuery<Cliente[], Error>({
    queryKey: ['clientes'],
    queryFn: fetchClientes,
    staleTime: 1000 * 60 * 10,
  });

  const clientesMutation = useMutation<Cliente, Error, Omit<Cliente, 'id'>>({
    mutationFn: createCliente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['clientes'] });;
    },
  });

  return {
    clientes: clientesQuery.data ?? [],
    isLoading: clientesQuery.isLoading,
    isError: clientesQuery.isError,
    error: clientesQuery.error,
    createCliente: clientesMutation.mutate,
    isCreating: clientesMutation.status === 'pending',
    createError: clientesMutation.error,
  };
}
