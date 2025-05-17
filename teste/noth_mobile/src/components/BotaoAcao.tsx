import React from 'react';
import { Pressable, Text } from 'react-native';

interface BotaoAcaoProps {
  label: string;
  cor: 'verde' | 'azul' | 'vermelho';
  onPress: () => void;
}

const coresTailwind = {
  verde: 'bg-green-700',
  azul: 'bg-blue-600',
  vermelho: 'bg-red-600',
};

export default function BotaoAcao({ label, cor, onPress }: BotaoAcaoProps) {
  return (
    <Pressable
      onPress={onPress}
      className={`flex-1 rounded-lg py-3 items-center ${coresTailwind[cor]}`}
    >
      <Text className="text-white font-bold text-base">{label}</Text>
    </Pressable>
  );
}
