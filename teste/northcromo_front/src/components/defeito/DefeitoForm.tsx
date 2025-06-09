// src/app/components/componente/ComponenteFormComModal.tsx

const [erroNome, setErroNome] = useState<string | null>(null)
const [erroCategoria, setErroCategoria] = useState<string | null>(null)

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault()
  setErroNome(null)
  setErroCategoria(null)

  if (!nome.trim()) {
    setErroNome('Digite o nome do componente')
    return
  }
  if (!selectedCategoriaId) {
    setErroCategoria('Selecione uma categoria')
    return
  }
  onSave(nome.toUpperCase(), selectedCategoriaId)
}

return (
  <>
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6">
      <input
        type="text"
        value={componenteId || ''}
        disabled
        placeholder="ID"
        className="sm:col-span-3 w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />
      <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value.toUpperCase())}
        placeholder="Nome do Componente"
        className="sm:col-span-6 w-full p-2 border border-gray-300 rounded-md"
      />
      {erroNome && <p className="text-red-500">{erroNome}</p>}

      <input
        type="text"
        value={selectedCategoriaNome}
        readOnly
        onClick={() => setModalAberto(true)}
        placeholder="Clique para selecionar categoria"
        className="sm:col-span-3 w-full p-2 border border-gray-300 rounded-md cursor-pointer bg-gray-100"
      />
      {erroCategoria && <p className="text-red-500">{erroCategoria}</p>}

      <div className="sm:col-span-12 flex gap-2">
        <button
          type="submit"
          className="flex items-center justify-center gap-2 px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 transition w-full"
        >
          {componenteId ? 'Atualizar' : 'Adicionar'}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-gray-400 text-white rounded-md hover:bg-gray-500 transition w-full"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>

    {/* Modal para seleção de categoria */}
    {modalAberto && (
      <div
        style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.4)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000,
        }}
        onClick={() => setModalAberto(false)}
      >
        <div
          style={{
            backgroundColor: 'white',
            borderRadius: 4,
            padding: 20,
            width: 320,
            maxHeight: '70vh',
            overflowY: 'auto',
            boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
            position: 'relative',
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <h3>Selecione uma categoria</h3>
          <button
            onClick={() => setModalAberto(false)}
            style={{
              position: 'absolute',
              top: 10,
              right: 20,
              background: 'none',
              border: 'none',
              fontSize: 24,
              cursor: 'pointer',
            }}
            aria-label="Fechar modal"
          >
            &times;
          </button>

          <ul style={{ listStyle: 'none', padding: 0, marginTop: 30 }}>
            {categoriasQuery.data!.map((c) => (
              <li
                key={c.id}
                onClick={() => selecionarCategoria(c)}
                style={{
                  padding: '8px 12px',
                  borderBottom: '1px solid #ddd',
                  cursor: 'pointer',
                  backgroundColor: selectedCategoriaId === c.id ? '#cce5ff' : undefined,
                }}
              >
                {c.nome}
              </li>
            ))}
          </ul>
        </div>
      </div>
    )}
  </>
)
