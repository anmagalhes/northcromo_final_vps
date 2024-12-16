// src/components/ClienteForm.tsx
import React, { useState } from 'react';

const ClienteForm: React.FC = () => {
  const [nome, setNome] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Formulário enviado:', nome);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Nome do Cliente:
        <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} />
      </label>
      <button type="submit">Enviar</button>
    </form>
  );
};

export default ClienteForm;
