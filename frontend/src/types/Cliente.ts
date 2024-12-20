// src/types/Cliente.ts
export interface Cliente {
  id?: number;
  nome: string | null;
  email: string | null;
  telefone: string | null;
  enviado?: boolean;
}
