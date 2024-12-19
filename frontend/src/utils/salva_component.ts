// src/utils/salva_component.ts
export const salva_component = (formType: string) => {
    // Seleciona o formulário com base no tipo informado (cliente ou fornecedor)
    const form = document.querySelector(`#${formType}-form`) as HTMLFormElement;
  
    if (!form) {
      console.error(`Formulário não encontrado: ${formType}-form`);
      return;
    }
  
    // Seleciona todos os inputs dentro do formulário
    const myInput = form.querySelectorAll('input') as NodeListOf<HTMLInputElement>;
  
    // Criando o objeto para armazenar os dados
    const obj_para_lancar: { [key: string]: string } = {};
  
    // Iterando sobre cada item encontrado e preenchendo o objeto
    myInput.forEach((item) => {
      obj_para_lancar[item.id] = item.value;
    });
  
    // Exibindo o objeto no console (aqui você pode enviar os dados para o backend)
    console.log(obj_para_lancar);
  }
  