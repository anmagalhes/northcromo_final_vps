// src/components/RecebimentoTable.tsx
"use client";

import React from "react";
import { ReactTabulator } from "react-tabulator";
import "tabulator-tables/dist/css/tabulator.min.css";

type RowData = {
  idOrdem: string;
  dataCadastro: string;
  nomeCliente: string;
  codProduto: string;
  qtdProduto: string;
  nomeProduto: string;
  notaInterna: string;
  referenciaProduto: string;
  op: string;
  queixaCliente: string;
  idPCP: string;
  nomeCompleto: string;
};

const data: RowData[] = [
  {
    idOrdem: "0001",
    dataCadastro: "2025-05-01",
    nomeCliente: "Empresa X",
    codProduto: "123",
    qtdProduto: "5",
    nomeProduto: "Produto Y",
    notaInterna: "Nota A",
    referenciaProduto: "Ref-001",
    op: "OP-001",
    queixaCliente: "Sem defeito",
    idPCP: "PCP001",
    nomeCompleto: "João da Silva",
  },
  // Adicione mais linhas conforme necessário
];

const columns = [
  { title: "Nº Controle", field: "idOrdem", hozAlign: "center" },
  { title: "Data Recebimento", field: "dataCadastro", hozAlign: "center" },
  {
  title: "Cliente",
  field: "nomeCliente",
  hozAlign: "center",
  headerSort: true,
},
  { title: "Cód", field: "codProduto", hozAlign: "center" },
  { title: "Qtda", field: "qtdProduto", hozAlign: "center" },
  { title: "Desc Serviço/ Produto / Tarefa", field: "nomeProduto", hozAlign: "left" },
  { title: "Nota", field: "notaInterna", hozAlign: "center" },
  { title: "Referência Produto", field: "referenciaProduto", hozAlign: "center" },
  { title: "Op", field: "op", visible: false },
  { title: "Observação", field: "queixaCliente", hozAlign: "left" },
  { title: "Id PCP", field: "idPCP", visible: false },
];

export default function RecebimentoTable() {
  return (
    <div className="tabulator-container">
      <ReactTabulator
        data={data}
        columns={columns}
        options={{
          pagination: "local",
          paginationSize: 300,
          paginationInitialPage: 1,
          movableColumns: true,
          initialSort: [
            { column: "dataCadastro", dir: "asc" },
            { column: "op", dir: "asc" },
          ],
        }}
        className="tabulator"
        layout="fitColumns"
      />
    </div>
  );
}
