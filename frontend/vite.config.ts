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
  build: {
    // Otimizações de produção
    outDir: 'dist',  // Pasta onde os arquivos de build vão ser colocados
    sourcemap: false,  // Não gerar map de fontes em produção
    chunkSizeWarningLimit: 500,  // Limitar o tamanho dos chunks para evitar erros de tamanho excessivo

    // Rollup (usado internamente pelo Vite) para otimização de pacotes
    rollupOptions: {
      output: {
        manualChunks: {
          // Exemplo de separação dos pacotes para otimizar cache
          vendor: ['react', 'react-dom', 'react-router-dom'],
        },
      },
    },

    // Cache para builds de produção
    minify: 'esbuild',  // Usar o esbuild para uma minificação muito rápida

    // Habilitar a compressão dos arquivos (gzip) para produção
    brotliSize: false,  // Desabilitar o cálculo de tamanho do brotli, útil para grandes projetos
  },
  server: {
    // Configuração para o ambiente de desenvolvimento
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000', // Apenas para desenvolvimento
    },
  },
});
