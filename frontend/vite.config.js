import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host:'0.0.0.0',
    port:5173,
    allowedHosts: ['xwleaderboard.amanshah2711.me'],
//    proxy: {
//      '/api': {
//           target: 'http://xwleaderboardbackend:5000',
//           changeOrigin: true,
//           secure: false,      
//           ws: false,
//       }
//  }

  },
});
