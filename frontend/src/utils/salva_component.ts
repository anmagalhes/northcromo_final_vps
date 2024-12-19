// src/utils/salva_component.ts
export const salva_component = (formType: string, data: any) => {
  // Seleciona o formulário com base no tipo informado (Ajustado para garantir que o id correto seja passado)
  const form = document.querySelector(`#${formType}-form`) as HTMLFormElement;

  if (!form) {
    console.error(`Formulário não encontrado: ${formType}-form`);
    return;
  }

  // Seleciona todos os inputs dentro do formulário com a classe 'my-input'
  const myInput = form.querySelectorAll('.my-input') as NodeListOf<HTMLInputElement>;

  // Criando o objeto para armazenar os dados do formulário
  const obj_para_lancar: { [key: string]: string } = {};

  // Iterando sobre cada item encontrado e preenchendo o objeto
  myInput.forEach((item) => {
    obj_para_lancar[item.id] = item.value;  // Usando o 'id' do input como chave
  });

  // Exibindo os dados coletados no formulário para teste
  console.log("Dados do formulário:", obj_para_lancar);

  // Salvando os dados no localStorage
  localStorage.setItem(`${formType}-form`, JSON.stringify(obj_para_lancar));
  console.log(`${formType}-form salvo no localStorage:`, obj_para_lancar);

  // Caso queira salvar dados gerais (como uma lista de clientes, por exemplo):
  if (data) {
    localStorage.setItem(formType, JSON.stringify(data));
    console.log(`${formType} salvo no localStorage:`, data);
  }
};
