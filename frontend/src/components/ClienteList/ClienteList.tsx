// src/components/ClienteList/ClienteList.tsx
import React from 'react';
import axios from 'axios';
import { Cliente } from '../../types/Cliente';  // Certifique-se de importar corretamente

interface ClienteListProps {
  clientes: Cliente[];  // Usando o tipo correto para o array de clientes
  onDelete: (id: number) => void;
}

const ClienteList: React.FC<ClienteListProps> = ({ clientes, onDelete }) => {
  const [clientes, setClientes] = useState<Cliente[]>([]);

  useEffect(() => {
    // Fazer a requisição para buscar os clientes do backend Flask
    axios.get('https://northcromocontrole.com.br/api/clientes')  // Usando o endpoint de produção
      .then(response => {
        setClientes(response.data);
      })
      .catch(error => {
        console.error('Erro ao buscar clientes:', error);
      });
  }, []); // O array vazio [] garante que a requisição seja feita apenas uma vez ao carregar o componente.


  return (
    <div>
      <ul>
        {clientes.map(cliente => (
          <li key={cliente.id}>
            {cliente.nome} - {cliente.email} - {cliente.telefone}
            <button onClick={() => onDelete(cliente.id)}>Excluir</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ClienteList;
