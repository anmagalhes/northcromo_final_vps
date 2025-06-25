'use client'
import { ReactNode } from 'react'

interface BotaoAcaoProps {
  label: string
  cor: 'verde' | 'azul' | 'vermelho' | 'cinza'
  onPress: () => void
  disabled?: boolean
  icone?: ReactNode
  className?: string
}

const coresTailwind = {
  verde: 'bg-green-600 hover:bg-green-700',
  azul: 'bg-blue-600 hover:bg-blue-700',
  vermelho: 'bg-red-600 hover:bg-red-700',
  cinza: 'bg-gray-500 hover:bg-gray-600',
  disabled: 'bg-gray-400 cursor-not-allowed'
}

export default function BotaoAcao({
  label,
  cor,
  onPress,
  disabled = false,
  icone,
  className = ''
}: BotaoAcaoProps) {
  return (
    <button
      onClick={onPress}
      disabled={disabled}
      className={`
        rounded-lg py-3 px-4 text-center transition-colors
        ${disabled ? coresTailwind.disabled : coresTailwind[cor]}
        text-white font-medium text-base
        flex items-center justify-center gap-2
        ${className}
      `}
    >
      {icone && <span className="text-lg">{icone}</span>}
      {label}
    </button>
  )
}
