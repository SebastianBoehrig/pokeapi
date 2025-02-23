import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
// import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [ sveltekit(), tailwindcss()],
	// server: {
	// 	proxy: {
	// 		'/api': 'http://localhost:8181/'
	// 	}
	// }
});
