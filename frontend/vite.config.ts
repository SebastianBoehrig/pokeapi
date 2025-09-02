import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [ sveltekit(), tailwindcss()],
	server: {
    host: '0.0.0.0',  // Required for Docker
    port: 5173,       // Container port
    hmr: {
      clientPort: 8080, // Tell HMR client to use the host-mapped port
    },
    watch: {
      usePolling: true // Needed for file watching in Docker
    }
  }
});
