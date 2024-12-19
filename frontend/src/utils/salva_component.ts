// src/utils/salva_component.ts
export const salva_component = (formType: string) => {

  // Seleciona o formulário com base no tipo informado (geral)
  const form = document.querySelector(`#${formType}-form`) as HTMLFormElement;

  if (!form) {
    console.error(`Formulário não encontrado: ${formType}-form`);
    return;
  }

  //
  // Seleciona todos os inputs dentro do formulário com a classe 'my-input'
  const myInput = form.querySelectorAll('.my-input') as NodeListOf<HTMLInputElement>;

  // Criando o objeto para armazenar os dados
  const obj_para_lancar: { [key: string]: string } = {};

  // Iterando sobre cada item encontrado e preenchendo o objeto
  myInput.forEach((item) => {
    obj_para_lancar[item.id] = item.value;  // Usando o 'id' do input para chave
  });

  // Exibindo o objeto no console para teste
  console.log("Dados do formulário:", obj_para_lancar);
}
