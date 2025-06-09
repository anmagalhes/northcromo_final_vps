"use client";

import React, { useEffect, useRef } from "react";
import { Tabulator } from "tabulator-tables";

interface Recebimento {
  numeroControle: string;
  dataRecebimento: string;
  horaRecebimento: string;
  cliente: string;
  quantidade: number;
  codigoProduto: string;
  nomeProduto: string;
  referencia: string;
  nfRemessa: string;
  observacao: string;
}

interface Props {
  dados: Recebimento[];
}

export default function RecebimentoTabela({ dados }: Props) {
  const tabelaRef = useRef<HTMLDivElement>(null);
  const tabulatorInstance = useRef<Tabulator | null>(null);

  useEffect(() => {
    if (!tabelaRef.current) return;

    if (tabulatorInstance.current) {
      tabulatorInstance.current.destroy();
    }

    tabulatorInstance.current = new Tabulator(tabelaRef.current, {
      data: dados,
      layout: "fitColumns",
      reactiveData: true,
      columns: [
        { title: "N° Controle", field: "numeroControle", width: 100 },
        { title: "Data Recebimento", field: "dataRecebimento", width: 130 },
        { title: "Hora Recebimento", field: "horaRecebimento", width: 130 },
        { title: "Cliente", field: "cliente", width: 150 },
        { title: "Quantidade", field: "quantidade", hozAlign: "right", width: 100 },
        { title: "Código Produto", field: "codigoProduto", width: 130 },
        { title: "Nome Produto", field: "nomeProduto", width: 150 },
        { title: "Referência", field: "referencia", width: 130 },
        { title: "NF Remessa", field: "nfRemessa", width: 130 },
        { title: "Observação", field: "observacao", width: 200 },
      ],
      pagination: "local",
      paginationSize: 5,
      paginationSizeSelector: [5, 10, 20],
      movableColumns: true,
      resizableRows: true,
      initialSort: [{ column: "numeroControle", dir: "asc" }],
    });

    return () => {
      tabulatorInstance.current?.destroy();
      tabulatorInstance.current = null;
    };
  }, [dados]);

  return <div ref={tabelaRef} className="tabulator" />;
}
