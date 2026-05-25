import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api/v1/bazi': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/api/v1/ziwei': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
      '/api/v1/relation': {
        target: 'http://localhost:8004',
        changeOrigin: true,
      },
      '/api/v1/fengshui': {
        target: 'http://localhost:8005',
        changeOrigin: true,
      },
      '/api/v1/oasis': {
        target: 'http://localhost:8007',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
