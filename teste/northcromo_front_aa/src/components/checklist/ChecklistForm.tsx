'use client';

import React, { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';

export interface Checklist {
  id: number;
  recebimento_id: string;
  descricao: string;
}

interface ChecklistFormProps {
  checklistId?: number;
  recebimentoId: number | string;
  setRecebimentoId: React.Dispatch<React.SetStateAction<number | string>>;
  descricao: string;
  loading: boolean;
  setDescricao: React.Dispatch<React.SetStateAction<string>>;
  temPdf: boolean;
  setTemPdf: React.Dispatch<React.SetStateAction<boolean>>;
  recebimentosOptions: string[];
  onSave: (
    recebimentoId: string,
    descricao: string,
    dataCadastro: string
  ) => void;
  onCancel?: () => void;
}

export default function ChecklistForm({
  checklistId,
  recebimentoId,
  descricao,
  recebimentosOptions,
  onSave,
  onCancel,
}: ChecklistFormProps) {
  // Converter recebimentoId para string para compatibilidade com Yup e useForm
  const recebimentoIdStr = String(recebimentoId);

  const schema = Yup.object({
    recebimentoId: Yup.string()
      .required('Recebimento ID é obrigatório')
      .oneOf(recebimentosOptions, 'Recebimento ID inválido'),
    descricao: Yup.string().required('Descrição é obrigatória'),
  }).required();

  const {
    control,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      recebimentoId: recebimentoIdStr,
      descricao,
    },
  });

  const [dataCadastro] = React.useState(() => {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const spOffset = -3 * 60 * 60000;
    const spDate = new Date(utc + spOffset);
    return spDate.toISOString();
  });

  useEffect(() => {
    setValue('recebimentoId', recebimentoIdStr);
    setValue('descricao', descricao);
  }, [recebimentoIdStr, descricao, setValue]);

  const onSubmit = (data: { recebimentoId: string; descricao: string }) => {
    onSave(data.recebimentoId, data.descricao, dataCadastro);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6"
      noValidate
    >
      <div className="sm:col-span-5">
        <Controller
          name="recebimentoId"
          control={control}
          render={({ field }) => (
            <>
              <input
                {...field}
                list="recebimentos-list"
                placeholder="Recebimento ID"
                className="w-full p-2 border border-green-300 rounded-md"
                autoComplete="off"
              />
              <datalist id="recebimentos-list">
                {recebimentosOptions.map((r) => (
                  <option key={r} value={r} />
                ))}
              </datalist>
              {errors.recebimentoId && (
                <p className="text-red-600 font-semibold">
                  {errors.recebimentoId.message}
                </p>
              )}
            </>
          )}
        />
      </div>

      <div className="sm:col-span-5">
        <Controller
          name="descricao"
          control={control}
          render={({ field }) => (
            <>
              <input
                {...field}
                placeholder="Descrição"
                className="w-full p-2 border border-green-300 rounded-md"
                autoComplete="off"
              />
              {errors.descricao && (
                <p className="text-red-600 font-semibold">
                  {errors.descricao.message}
                </p>
              )}
            </>
          )}
        />
      </div>

      <div className="flex-1 flex gap-3 items-center">
        <button
          type="submit"
          className="px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800"
        >
          {checklistId ? 'Atualizar' : 'Adicionar'}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}
