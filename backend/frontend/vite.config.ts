import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@components': path.resolve(__dirname, './src/components'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000', // Apenas para desenvolvimento
    },
  },
  build: {
    // Produção usa variáveis de ambiente
    define: {
      'process.env.API_URL': JSON.stringify(process.env.VITE_API_URL),
    },
  },
});

