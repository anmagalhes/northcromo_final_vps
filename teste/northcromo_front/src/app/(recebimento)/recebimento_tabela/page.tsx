import RecebimentoTabela from "@/components/recebimento/Recebimentotabela";

const dadosExemplo = [
  {
    numeroControle: "001",
    dataRecebimento: "2025-05-24",
    horaRecebimento: "14:30",
    cliente: "Cliente Exemplo",
    quantidade: 10,
    codigoProduto: "ABC123",
    nomeProduto: "Produto X",
    referencia: "Ref-01",
    nfRemessa: "NF123456",
    observacao: "Sem observações",
  },
  {
    numeroControle: "002",
    dataRecebimento: "2025-05-25",
    horaRecebimento: "15:00",
    cliente: "Cliente Dois",
    quantidade: 5,
    codigoProduto: "DEF456",
    nomeProduto: "Produto Y",
    referencia: "Ref-02",
    nfRemessa: "NF654321",
    observacao: "Urgente",
  },
];

export default function Home() {
  return (
    <main>
      <h1 className="text-3xl font-bold mb-6">Tabela de Recebimentos</h1>
      <RecebimentoTabela dados={dadosExemplo} />
    </main>
  );
}
