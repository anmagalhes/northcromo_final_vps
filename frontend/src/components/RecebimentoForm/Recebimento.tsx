import React, { useState } from 'react';
import { Recebimento } from 'src/types/Recebimento'; // Tipo Recebimento
import { salva_component } from '@utils/salva_component';

interface RecebimentoFormProps {
  onRecebimentoAdicionado: (recebimento: Recebimento) => void; // Função passada via props para adicionar o recebimento
}

const RecebimentoForm: React.FC<RecebimentoFormProps> = ({ onRecebimentoAdicionado }) => {
  const [numeroControle, setNumeroControle] = useState<string>('');
  const [dataRecebimento, setDataRecebimento] = useState<string>('');
  const [idCliente, setIdCliente] = useState<string>('');
  const [quantidade, setQuantidade] = useState<number>(1);
  const [codigoProduto, setCodigoProduto] = useState<string>('');
  const [notaInterna, setNotaInterna] = useState<string>('');
  const [numeroReferencia, setNumeroReferencia] = useState<string>('');
  const [idVendedor, setIdVendedor] = useState<string>('');
  const [queixaCliente, setQueixaCliente] = useState<string>('');

  // Função chamada no envio do formulário
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Instanciando o novo recebimento com base nos dados do formulário
    const novoRecebimento: Recebimento = {
      id: Date.now(),
      numeroControle,
      dataRecebimento,
      idCliente,
      quantidade,
      codigoProduto,
      notaInterna,
      numeroReferencia,
      idVendedor,
      queixaCliente,
    };

    // Chama a função passada via props para adicionar o recebimento no componente pai
    onRecebimentoAdicionado(novoRecebimento);

    // Salva o novo recebimento no localStorage
    salva_component('recebimentos', novoRecebimento);

    // Limpa os campos após o envio
    setNumeroControle('');
    setDataRecebimento('');
    setIdCliente('');
    setQuantidade(1);
    setCodigoProduto('');
    setNotaInterna('');
    setNumeroReferencia('');
    setIdVendedor('');
    setQueixaCliente('');
  };

  return (
    <form id="recebimento-form" onSubmit={handleSubmit}>
      <input
        type="text"
        id="numeroControle"
        className="my-input"
        placeholder="Número de Controle"
        value={numeroControle}
        onChange={(e) => setNumeroControle(e.target.value)}
      />
      <input
        type="date"
        id="dataRecebimento"
        className="my-input"
        value={dataRecebimento}
        onChange={(e) => setDataRecebimento(e.target.value)}
      />
      <input
        type="text"
        id="idCliente"
        className="my-input"
        placeholder="ID Cliente"
        value={idCliente}
        onChange={(e) => setIdCliente(e.target.value)}
      />
      <input
        type="number"
        id="quantidade"
        className="my-input"
        placeholder="Quantidade"
        value={quantidade}
        onChange={(e) => setQuantidade(Number(e.target.value))}
      />
      <input
        type="text"
        id="codigoProduto"
        className="my-input"
        placeholder="Código do Produto"
        value={codigoProduto}
        onChange={(e) => setCodigoProduto(e.target.value)}
      />
      <input
        type="text"
        id="notaInterna"
        className="my-input"
        placeholder="Nota Interna"
        value={notaInterna}
        onChange={(e) => setNotaInterna(e.target.value)}
      />
      <input
        type="text"
        id="numeroReferencia"
        className="my-input"
        placeholder="Número de Referência"
        value={numeroReferencia}
        onChange={(e) => setNumeroReferencia(e.target.value)}
      />
      <input
        type="text"
        id="idVendedor"
        className="my-input"
        placeholder="ID Vendedor"
        value={idVendedor}
        onChange={(e) => setIdVendedor(e.target.value)}
      />
      <input
        type="text"
        id="queixaCliente"
        className="my-input"
        placeholder="Queixa do Cliente"
        value={queixaCliente}
        onChange={(e) => setQueixaCliente(e.target.value)}
      />

      <button type="submit">Adicionar Recebimento</button>
    </form>
  );
};

export default RecebimentoForm;
