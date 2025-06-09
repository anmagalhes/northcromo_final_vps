import { FiEdit, FiTrash2 } from 'react-icons/fi';

interface DefeitoTableProps {
  defeitos: Defeito[];
  selecionados: number[];
  toggleSelecionado: (id: number) => void;
  toggleSelecionarTodos: () => void;
  todosSelecionados: boolean;
  idEditar: number | null;
  modoEdicaoMultipla: boolean;
  editaveis: Defeito[];
  setEditaveis: React.Dispatch<React.SetStateAction<Defeito[]>>;
  onEdit: (item: Defeito) => void;
  onDelete: (id: number) => void;
  onSalvarEdicao: (itemEditado: Defeito) => void;
  onCancelarEdicao: () => void;
  componentes: { id: number, componente_nome: string }[]; // Passando os componentes para o select
  onDeleteEmMassa: (ids: number[]) => void; // Função para excluir múltiplos
  onEditarEmMassa: (itens: Defeito[]) => void; // Função para editar múltiplos
}

export default function DefeitoTable({
  defeitos,
  selecionados,
  toggleSelecionado,
  toggleSelecionarTodos,
  todosSelecionados,
  idEditar,
  modoEdicaoMultipla,
  editaveis,
  setEditaveis,
  onEdit,
  onDelete,
  onSalvarEdicao,
  onCancelarEdicao,
  componentes,
  onDeleteEmMassa,
  onEditarEmMassa,
}: DefeitoTableProps) {

  // Função para atualizar campos na edição
  const handleChangeEditavel = (id: number, campo: keyof Defeito, valor: any) => {
    setEditaveis(prev =>
      prev.map(item =>
        item.id === id ? { ...item, [campo]: valor } : item
      )
    );
  };

  // Função para editar múltiplos defeitos ao mesmo tempo
  const handleEditarEmMassa = () => {
    const itensSelecionados = editaveis.filter(item => selecionados.includes(item.id));
    if (itensSelecionados.length > 0) {
      onEditarEmMassa(itensSelecionados);
    }
  };

  // Função para excluir múltiplos defeitos ao mesmo tempo
  const handleExcluirEmMassa = () => {
    onDeleteEmMassa(selecionados);
  };

  return (
    <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2 text-left">
              <input
                type="checkbox"
                checked={todosSelecionados}
                onChange={toggleSelecionarTodos}
                className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
              />
            </th>
            <th className="px-4 py-2 text-left">Componente</th>
            <th className="px-4 py-2 text-left">Descrição do Defeito</th>
            <th className="px-4 py-2 text-left">Data</th>
            <th className="px-4 py-2 text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          {defeitos.length === 0 ? (
            <tr>
              <td colSpan={5} className="text-center p-4">
                Nenhum defeito cadastrado.
              </td>
            </tr>
          ) : (
            defeitos.map((defeito) => {
              const estaEditando = idEditar === defeito.id;
              const editavel = editaveis.find(e => e.id === defeito.id) || defeito;
              const dataISO = editavel.data ? new Date(editavel.data).toISOString().slice(0, 16) : '';

              return (
                <tr
                  key={defeito.id}
                  className={`hover:bg-gray-50 border-t border-gray-200 ${
                    estaEditando ? 'bg-yellow-100' : ''
                  }`}
                >
                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(defeito.id)}
                      onChange={() => toggleSelecionado(defeito.id)}
                      className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
                    />
                  </td>

                  <td className="px-4 py-2">
                    {estaEditando ? (
                      <select
                        value={editavel.componente_id}
                        onChange={e => handleChangeEditavel(defeito.id, 'componente_id', Number(e.target.value))}
                        className="border rounded px-2 py-1 w-full"
                      >
                        {componentes.map(comp => (
                          <option key={comp.id} value={comp.id}>
                            {comp.componente_nome}
                          </option>
                        ))}
                      </select>
                    ) : (
                      defeito.componente_nome
                    )}
                  </td>

                  <td className="px-4 py-2">
                    {estaEditando ? (
                      <input
                        type="text"
                        value={editavel.def_nome}
                        onChange={e => handleChangeEditavel(defeito.id, 'def_nome', e.target.value)}
                        className="border rounded px-2 py-1 w-full"
                      />
                    ) : (
                      defeito.def_nome
                    )}
                  </td>

                  <td className="px-4 py-2">
                    {estaEditando ? (
                      <input
                        type="datetime-local"
                        value={dataISO}
                        onChange={e => {
                          const valor = new Date(e.target.value).toISOString();
                          handleChangeEditavel(defeito.id, 'data', valor);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      />
                    ) : (
                      new Date(defeito.data).toLocaleString()
                    )}
                  </td>

                  <td className="px-4 py-2 text-center flex gap-3">
                    {estaEditando ? (
                      <>
                        <button
                          onClick={() => onSalvarEdicao(editavel)}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          Salvar
                        </button>
                        <button
                          onClick={onCancelarEdicao}
                          className="text-red-600 hover:text-red-800"
                        >
                          Cancelar
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => onEdit(defeito)}
                          className="text-blue-600 hover:text-blue-800"
                          title="Editar"
                        >
                          <FiEdit />
                        </button>
                        <button
                          onClick={() => onDelete(defeito.id)}
                          className="text-red-600 hover:text-red-800"
                          title="Excluir"
                        >
                          <FiTrash2 />
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>

      {/* Botões de ações em massa */}
      {modoEdicaoMultipla && (
        <div className="flex gap-4 mt-4">
          <button
            onClick={handleExcluirEmMassa}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-800"
          >
            Excluir Selecionados
          </button>
          <button
            onClick={handleEditarEmMassa}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-800"
          >
            Editar Selecionados
          </button>
        </div>
      )}
    </div>
  );
}
