import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@components': path.resolve(__dirname, './src/components'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@utils': path.resolve(__dirname, './src/utils'),
    }
  },
  server: {
    port: 3000, // Porta do servidor de desenvolvimento
    proxy: {
      // Para desenvolvimento, se a API estiver rodando em localhost:5000
      '/api': 'http://localhost:5000', // Substitua localhost:5000 pela sua API local
    },
  },
  // Configuração para produção
  build: {
    // Em produção, as requisições irão para o domínio correto
    define: {
      'process.env.API_URL': JSON.stringify('https://northcromocontrole.com.br/api'),
    },
  },
})
