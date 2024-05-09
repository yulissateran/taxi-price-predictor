import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 8080, // Set the production port here
    host: true,
  },
  preview: {
    port: 8080,
    host: true,
  },
});
